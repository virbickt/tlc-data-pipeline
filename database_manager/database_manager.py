import os
import time

import pyodbc
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Database:
    def __init__(
        self, subscription_id: str, client_id: str, client_secret: str, tenant_id: str
    ) -> None:
        self.subscription_id = subscription_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id

    def get_clients(self) -> None:
        """
        Authenticates the service principal to get the clients required to create server and database.

        :returns: None
        :rtype: NoneType
        """

        credentials = ServicePrincipalCredentials(
            client_id=self.client_id, secret=self.client_secret, tenant=self.tenant_id
        )

        resource_client = ResourceManagementClient(credentials, self.subscription_id)
        sql_client = SqlManagementClient(credentials, self.subscription_id)

        return resource_client, sql_client

    def create_resource_group(
        self, group_name: str = "sample-rg", region: str = "northeurope"
    ) -> None:
        """
        Creates a new resource group.

        :param group_name str: the name for the new resource group that is to be created.
        :param region str: region which the new resource group is going to be assigned to. To list all the available regions in the accessible format, use 'az account list-locations -o table' on Azure CLI.
        :returns: None
        :rtype: NoneType
        """

        resource_client, _ = self.get_clients()
        print(f"Creating a new resource group '{group_name}' ({region})...\n")
        resource_client.resource_groups.create_or_update(
            group_name, {"location": region}
        )
        print(f"Resource group '{group_name}' created successfully.\n")

    def create_server(
        self,
        server_name: str = "sample-server",
        administrator_login: str = "admin",
        administrator_login_password: str = "please_God_just_make_this_work",
        group_name: str = "tlc-data-rg",
        region: str = "northeurope",
    ) -> None:
        """
        Creates a new server.

        :param server_name str: the name for the server
        :param group_name str: the name for the new resource group that is to be created.
        :param region str: region which the new resource group is going to be assigned to. To list all the available regions in the accessible format, use 'az account list-locations -o table' on Azure CLI.
        :returns: None
        :rtype: NoneType
        """
        _, sql_client = self.get_clients()
        print(f"Creating a new server '{server_name}' ({region})...\n")

        server = sql_client.servers.create_or_update(
            group_name,
            server_name,
            {
                "location": region,
                "version": "12.0",  # Required for create
                "administrator_login": os.getenv(
                    "ADMINISTRATOR_LOGIN"
                ),  # Required for create
                "administrator_login_password": os.getenv(
                    "ADMINISTRATOR_LOGIN_PASSWORD"
                ),  # Required for create
            },
        )
        print(f"Server '{server_name}' created successfully.\n")

    def create_database(
        self,
        group_name: str = "tlc-data-rg",
        server_name: str = "tlc-data-server",
        database_name: str = "tlc-data-db",
        region: str = "northeurope",
        collation: str = "SQL_Latin1_General_CP1_CI_AS",
        pricing_tier: str = "S0",
    ) -> None:
        """
        Creates a new SQL database.

        :param group_name str: the name for the new resource group that the database to be created will belong to.
        :param server_name str: the name of the server that will host the database to be created.
        :param database_name str: the naem for the database to be created.
        :param region str: region which the new resource group is going to be assigned to. To list all the available regions in the accessible format, use 'az account list-locations -o table' on Azure CLI.
        :param collation str: type of collation to be used. Collations determine sorting rules as well as case/accent sensitivity for the data which means that the results of the exactly same query might differ when it is on databases with different collations. For the types of collations available, please refer to https://docs.microsoft.com/en-us/sql/relational-databases/collations/collation-and-unicode-support?view=sql-server-ver15.
        :param pricing_tier str: the pricing tier for the database to be created. Pricing tier determines fixed amount of compute resource that is to be allocated to the database for a fixed price billed hourly.
        :returns: None
        :rtype: NoneType
        """
        _, sql_client = self.get_clients()
        print(f"Creating a new database '{database_name}' ({region})...\n")
        database = sql_client.databases.create_or_update(
            group_name,
            server_name,
            database_name,
            {
                "location": region,
                "collation": collation,
                "create_mode": "default",
                "requested_service_objective_name": pricing_tier,
            },
        )
        print(f"Database '{database_name}' created successfully.\n")

    def whitelist_ip(
        self,
        rule_name: str = "test-rule",
        resource_group: str = "tlc-data-rg",
        server_name: str = "tlc-data-server",
        ip_address: str = "88.118.83.237",
    ) -> None:
        """
        Add the given IP adress to the list of IP adressess that have access to the database. While the indended use case is adding a single IP address, it is originally intended to whitelist a range of IP adresses. This is useful for cases when IP adress change as it would still fall inside the range of the whitelisted IP addresses.

        :param group_name str: the name for the new resource group that the database belongs to.
        :param server_name str: the name of the database that the access is to be granted to.
        :param ip_address str: the IP address to grant the access to the database.
        :returns: None
        :rtype: NoneType
        """
        print(f"Creating a new firewall rule '{rule_name}'...")
        os.system(
            f"az sql server firewall-rule create --name {rule_name} --resource-group {resource_group} --server {server_name} --start-ip-address {ip_address} --end-ip-address {ip_address}"
        )
        print("\nWaiting for whitelisting of IP to take effect...")
        time.sleep(60)

    def encrypt_database(
        self,
        server_name: str = "sample-server",
        database_name: str = "sample-database",
        login_username: str = "secretagent",
        login_password: str = "please_God_just_make_this_work",
        encryption_password: str = "abcdefg123456ABCDEFG",
        driver: int = 17,
    ) -> None:
        """
        Encrypt the database.

        :param server_name str: the name of the server that hosts the database to be encrypted.
        :param database_name str: the name of the database that is to be encrypted.
        :param login_username str: the login username for the database which was set when creating the database.
        :param login_password str: the password for the database which was set when creating the database.
        :param encryption_password str: the password used for the encryption of the database.
        :param driver int: ODBC driver version. The default version is ODBC Driver 17 for SQL Server.
        :returns: None
        :rtype: NoneType
        """
        query = f"CREATE MASTER KEY ENCRYPTION BY PASSWORD = '{encryption_password}'"
        with pyodbc.connect(
            "DRIVER="
            + f"{{ODBC Driver {driver} for SQL Server}}"
            + ";SERVER=tcp:"
            + f"{server_name}.database.windows.net"
            + ";PORT=1433;DATABASE="
            + database_name
            + ";UID="
            + os.getenv("ADMINISTRATOR_LOGIN")
            + ";PWD="
            + os.getenv("ADMINISTRATOR_LOGIN_PASSWORD")
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

    def create_credentials(
        self,
        server_name: str = "sample-server",
        database_name: str = "sample-database",
        login_username: str = "secretagent",
        login_password: str = "please_God_just_make_this_work",
        driver: int = 17,
        sas_token: str = "'sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2022-01-20T04:01:24Z&st=2022-01-08T20:01:24Z&spr=https&sig=ymHDIq%2FKSemvQFeGQwR%2FFifUX3yyQNdH8N7l9QNNq7U%3D'",
    ) -> None:
        """
        Encrypt the database.

        :param server_name str: the name of the server that hosts the database to be encrypted.
        :param database_name str: the name of the database that is to be encrypted.
        :param login_username str: the login username for the database which was set when creating the database.
        :param login_password str: the password for the database which was set when creating the database.
        :param sas_token str: shared access signature (SAS) which is required to be generated using Azure Platform prior to executing the function.
        :param driver int: ODBC driver version. The default version is ODBC Driver 17 for SQL Server.
        :returns: None
        :rtype: NoneType
        """
        query = f"""
            CREATE DATABASE SCOPED CREDENTIAL BlobCredential
            WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
            SECRET = {sas_token};
            """
        with pyodbc.connect(
            "DRIVER="
            + f"{{ODBC Driver {driver} for SQL Server}}"
            + ";SERVER=tcp:"
            + f"{server_name}.database.windows.net"
            + ";PORT=1433;DATABASE="
            + database_name
            + ";UID="
            + os.getenv("ADMINISTRATOR_LOGIN")
            + ";PWD="
            + os.getenv("ADMINISTRATOR_LOGIN_PASSWORD")
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

    def create_external_data_source(
        self,
        server_name: str = "sample-server",
        database_name: str = "sample-database",
        login_username: str = "secretagent",
        login_password: str = "please_God_just_make_this_work",
        driver: int = 17,
        datasource_name: str = "sample-datasource",
        container_name: str = "tlc-data",
        location: str = "storageassessmentmacaw",
    ) -> None:
        """
        Creates an external data source.

        :param server_name str: the name of the server that hosts the database to be encrypted.
        :param database_name str: the name of the database that is to be encrypted.
        :param login_username str: the login username for the database which was set when creating the database.
        :param login_password str: the password for the database which was set when creating the database.
        :param driver int: ODBC driver version. The default version is ODBC Driver 17 for SQL Server.
        :param datasource_name: custom name for the external datasource which is to be used to upload data to the database.
        :param location str: the name of the storage which is required to be created prior to executing the function.
        :param container_name str: the name of the container which is to be established as an external data source.
        :returns: None
        :rtype: NoneType
        """

        datasource_name = f"'{datasource_name}'"
        location = f"'https://{location}.blob.core.windows.net/{container_name}'"

        query = f"""
          CREATE EXTERNAL DATA SOURCE AzureBlob
              WITH ( 
                  TYPE       = BLOB_STORAGE,
                  LOCATION   = {location},
                  CREDENTIAL = BlobCredential
              );
          """

        with pyodbc.connect(
            "DRIVER="
            + f"{{ODBC Driver {driver} for SQL Server}}"
            + ";SERVER=tcp:"
            + f"{server_name}.database.windows.net"
            + ";PORT=1433;DATABASE="
            + database_name
            + ";UID="
            + login_username
            + ";PWD="
            + login_password
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

    def create_table(
        self,
        server_name: str = "sample-server",
        database_name: str = "sample-database",
        login_username: str = "secretagent",
        login_password: str = "please_God_just_make_this_work",
        driver: int = 17,
        table_name: str = "tlc_data",
    ) -> None:
        """
        Creates a new table

        :param server_name str: the name of the server that hosts the database to be encrypted.
        :param database_name str: the name of the database that is to be encrypted.
        :param login_username str: the login username for the database which was set when creating the database.
        :param login_password str: the password for the database which was set when creating the database.
        :param driver int: ODBC driver version. The default version is ODBC Driver 17 for SQL Server.
        :param table_name str: the name for the table that is to be newly created inside the database
        """
        query = f"""
                        DROP TABLE IF EXISTS {table_name};

                        CREATE TABLE {table_name} (
                        VendorID int,
                        tpep_pickup_datetime datetime,
                        tpep_dropoff_datetime datetime,
                        passenger_count int,
                        trip_distance float,
                        RatecodeID int,
                        store_and_fwd_flag char,
                        PULocationID int,
                        DOLocationID int,
                        payment_type int,
                        fare_amount float,
                        extra	float,
                        mta_tax float,
                        tip_amount float,
                        tolls_amount float,
                        improvement_surcharge float,
                        total_amount float,
                        congestion_surcharge float
                        )
                        """
        print(f"Creating a table '{table_name}'...")

        with pyodbc.connect(
            "DRIVER="
            + f"{{ODBC Driver {driver} for SQL Server}}"
            + ";SERVER=tcp:"
            + f"{server_name}.database.windows.net"
            + ";PORT=1433;DATABASE="
            + database_name
            + ";UID="
            + os.getenv("ADMINISTRATOR_LOGIN")
            + ";PWD="
            + os.getenv("ADMINISTRATOR_LOGIN_PASSWORD"),
            fast_executemany=True,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
        print(f"Table '{table_name}' created successfully.")

    def load_csv_to_db(
        self,
        server_name: str = "sample-server",
        database_name: str = "sample-database",
        login_username: str = "secretagent",
        login_password: str = "please_God_just_make_this_work",
        driver: int = 17,
        table_name: str = "sample-table",
        file_name: str = "input.csv",
        data_source: str = "AzureBlob",
    ) -> None:
        """
        :param server_name str: the name of the server that hosts the database to be encrypted.
        :param database_name str: the name of the database that is to be encrypted.
        :param login_username str: the login username for the database which was set when creating the database.
        :param login_password str: the password for the database which was set when creating the database.
        :param driver int: ODBC driver version. The default version is ODBC Driver 17 for SQL Server.
        :param table_name str: the name for the table that is to be newly created inside the database
        """

        file_name = f"'{file_name}'"
        data_source = f"'{data_source}'"
        driver = 17

        query = f"""
                        BULK INSERT [dbo].[{table_name}]
                        FROM {file_name}
                        WITH ( 
                            DATA_SOURCE = 'AzureBlob',
                            FORMAT      = 'CSV',
                            FIRSTROW    = 2
                        );
                        """

        print(f"Inserting '{file_name}' into '{table_name}'...")

        with pyodbc.connect(
            "DRIVER="
            + f"{{ODBC Driver {driver} for SQL Server}}"
            + ";SERVER=tcp:"
            + f"{server_name}.database.windows.net"
            + ";PORT=1433;DATABASE="
            + database_name
            + ";UID="
            + os.getenv("ADMINISTRATOR_LOGIN")
            + ";PWD="
            + os.getenv("ADMINISTRATOR_LOGIN_PASSWORD"),
            fast_executemany=True,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

        print(f"Bulk insert of '{file_name}' has been successful.")
