# tlc-data-pipeline
This is an automated solution to collect [TLC Trip Record data](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and upload it to a database on Azure which was created as part of the Macaw Data Engineering Academy assessment task.  

1. [Introduction](#Prerequisites)
2. [Installation](#Installation)
3. [Methods](#Methods)
4. [Technologies](#Technologies)
5. [License](#License)
6. [Contact](#Contact)


## Preprequisites
In order for the script to be used without any problems, you need to have at least [Python 3.9](https://www.python.org/downloads/) installed. Additionally, [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) needs to be installed as the script executes CLI commands to whitelist your IP address which is for the storage account and database to be connected and the data to eventually be stored in in the database.

## Installation
The installation guide assumes that you're using Windows and have (GitBash)[https://git-scm.com/downloads] installed.  

1. Clone the repository using the terminal. Inside the terminal, run 
```
git clone https://github.com/virbickt/tlc-data-pipeline.git
```
A folder called "tlc-data-pipeline" will be created on your current folder. 

2. It's a good idea to create a virtual environment prior to installing all the dependencies. This can be done again using the terminal by running 
```
python -m venv .venv
```
3. Activate the virtual environment using the terminal:
```
source .venv/Scripts/activate
```
The packages that the script makes use of can be install via pip:
```python
pip install -r requirements.txt
```
4. Start the script using the terminal (as you would any other Python file)
```
python app.py
```

## Methods
### Collector
#### generate_urls
- `generate_urls()`
Generates a list of urls to collect the data from by iterating over the range of years that the `Collector` object has been inicialized with. If the number for the month consists in a single digit, it is appended with `0`.

    Returns : 
    - urls(List[str]): the list that contains urls for each month's data in `.csv` format
#### extract_data
- `extract_data(url, filename)`
Retrieves the content of the page which are then written into a `.csv` file which is saved by the name specified as `filename`.

    Parameters:
    - url(str): the url to retrieve the content from and write into a .csv file.
    - file_name(str): the name which is to be used to save the file with.

    Returns: 
    - None

## Methods
### FileManager
#### create_container
- `create_container(container_name)`
Creates a new container inside Azure Storage. 

    Parameters:
    - container_name(str): the name for the container to be created. Default value: "tlc-data-demo"

    Returns: 
    - None
#### upload_file
- `upload_file(container_name, file_name)`
Uploads the file to Azure Storage as a blob. Blobs, as they are referred to in Azure documentation, are Azure-specific objects that can hold text or binary data, including images, documents, etc.

    Parameters:
    - container_name(str): the name of a container created prior to uploading the file. Default value: "tlc-data-demo"
    - file_name(str): the name for the file (blob). This is the name that the file is going to be stored with in your storage account.

    Returns: 
    - None

### Database
#### create_container
- `get_clients()`
Authenticates the service principal to get the clients required to create server and database.

    Parameters:
    - None

    Returns: 
    - resource_client(ResourceManagementClient):
    - sql_client(SqlManagementClient):
#### create_resource_group
- `create_resource_group(group_name, region)`
Creates a new resource group.

    Parameters:
    - group_name(str): the name for the new resource group that is to be created.
    - region(str): region to which the new resource group is going to be assigned to. To list all the available regions in the accessible format, use `az account list-locations -o table` when using a terminal with Azure CLI installed.
    - administrator_login(str): the username for logging into the server as an administrator.
    - administrator_login_password(str): the password for logging into the server as an administrator.

    Returns: 
    - None
#### create_server
- `create_server()`
Creates a new server. If you intend to use the methods in isolation, be aware that a server must be created prior to creating a database.

    Parameters:
    - server_name(str): the name for the server
    - group_name(str): the name for the new resource group which has been created prior to creating a server.
    - region(str): region to which the new server is going to be assigned to. To list all the available regions in the accessible format, use `az account list-locations -o table` when using a terminal with Azure CLI installed.
    - administrator_login(str): the username for logging into the server as an administrator.
    - administrator_login_password(str): the password for logging into the server as an administrator.
    - 

    Returns: 
    - None
#### create_database
- `create_database()`
Creates a new SQL database.

    Parameters:
    - group_name(str): the name for the new resource group that the database to be created will belong to.
    - server_name(str): the name of the server that will host the database to be created. The server has to be created prior to creating a database.
    - database_name(str): the name for the database to be created.
    - region(str): region to which the new database is going to be assigned to. To list all the available regions in the accessible format, use `az account list-locations -o table` when using a terminal with Azure CLI installed. 
    - collation(str): type of collation to be used. Collations determine sorting rules as well as case/accent sensitivity for the data which means that the results of the exactly same query might differ when it is on databases with different collations. For the types of collations available, please refer to the [official docs](https://docs.microsoft.com/en-us/sql/relational-databases/collations/collation-and-unicode-support?view=sql-server-ver15).
    - pricing_tier(str): the pricing tier for the database to be created. Pricing tier determines fixed amount of compute resource that is to be allocated to the database for a fixed price billed hourly.

    Returns: 
    - None
#### whitelist_ip
- `whitelist_ip()`
Add the given IP adress to the list of IP adressess that have access to the database. While the indended use case is adding a single IP address, it is originally intended to whitelist a range of IP adresses. This is useful for cases when IP adress change as it would still fall inside the range of the whitelisted IP addresses.

    Parameters:
    - rule_name(str): the name for the firewall rule to be created.
    - group_name(str): the name for the new resource group that the server and database (both preferrably) belongs to.
    - server_name(str): the name of the server that the access is to be granted to.
    - ip_address(str): the IP address to grant the access to the database.

    Returns: 
    - None
#### encrypt_database
- `encrypt_database()`
Encrypt the database.

    Parameters:
    - server_name(str): the name of the server that hosts the database to be encrypted.
    - database_name(str): the name of the database that is to be encrypted.
    - login_username(str): the login username for the database which was set when creating the server to host the database.
    - login_password(str): the password for the database which was set when creating the server to host the database.
    - encryption_password(str): the password used for the encryption of the database.
    - driver(int): ODBC driver version. The default version is ODBC Driver 17 for SQL Server.

    Returns: 
    - None
#### create_credentials
- `create_credentials()`
Create the credentials which will be used to load the .csv files to the database from the storage account.

    Parameters:
    - credential_name(str): the name for the credential to be used to load the resources to the database from the storage account.
    - server_name(str): the name of the server hosting the database.
    - database_name(str): the name of the database that will be used to store the resources loaded from the storage account.
    - login_username(str): the login username for the database which was set when creating the server to host the database.
    - login_password(str): the password for the database which was set when creating the server to host the database.
    - sas_token(str): shared access signature (SAS) which is required to be generated using Azure Platform prior to executing the function.
    - driver(int): ODBC driver version. The default version is ODBC Driver 17 for SQL Server. 

    Returns: 
    - None
#### create_external_data_source
- `create_external_data_source()`
Creates an external data source.

    Parameters:
    - datasource_name(str): custom name for the external datasource which is to be used to upload data to the database.
    - credential_name(str): the name for the credential which will be used to create the external data source. Must be created prior to creating the external data source.
    - location(str): the name of the storage which is required to be created prior to executing the function.
    - container_name(str): the name of the container which is to be established as an external data source.
    - server_name(str): the name of the server hosting the database.
    - database_name(str): the name of the database that will be used to store the resources loaded from the storage account.
    - login_username(str): the login username for the database which was set when creating the server to host the database.
    - login_password(str): the password for the database which was set when creating the server to host the database.
    - driver(int): ODBC driver version. The default version is ODBC Driver 17 for SQL Server. 

    Returns: 
    - None
#### create_table
- `create_table()`
Creates a new table. Note that the schema provided is tailored specifically for NYC Taxi and Limousine Commission data.

    Parameters:
    - server_name(str): the name of the server that hosts the database.
    - database_name(str): the name of the database where the table is going to be created.
    - login_username(str): the login username for the database which was set when creating the server to host the database.
    - login_password(str): the password for the database which was set when creating the server to host the database.
    - driver(int): ODBC driver version. The default version is ODBC Driver 17 for SQL Server.
    - table_name(str): the name for the table to be created.

    Returns: 
    - None
#### load_csv_to_db
- `load_csv_to_db()`
Loads the .csv files taken from the storage and inserts the data to the table which is to be created prior to loading the data. 

    Parameters:
    - server_name(str): the name of the server that hosts the database.
    - database_name(str): the name of the database with the table.
    - login_username(str): the login username for the database which was set when creating the server to host the database.
    - login_password(str): the password for the database which was set when creating the server to host the database.
    - driver(int): ODBC driver version. The default version is ODBC Driver 17 for SQL Server.
    - table_name(str): the name for the table where the data is going to inserted.
    - file_name(str): the name of the blob inside the storage which is where the data is going to be taken from.

    Returns: 
    - None



## Technologies:
- `adal==1.2.7`
- `azure-common==1.1.4`
- `azure-core==1.21.1`
- `azure-identity==1.7.1`
- `azure-mgmt-core==1.3.0`
- `azure-mgmt-nspkg==3.0.2`
- `azure-mgmt-resource==0.31.0`
- `azure-mgmt-sql==0.2.0`
- `azure-mgmt-storage==19.0.0`
- `azure-nspkg==3.0.2`
- `azure-storage-blob==12.9.0`
- `certifi==2021.10.8`
- `cffi==1.15.0`
- `charset-normalizer==2.0.10`
- `colorama==0.4.4`
- `cryptography==36.0.1`
- `humanize==3.13.1`
- `idna==3.3`
- `isodate==0.6.1`
- `msal==1.16.0`
- `msal-extensions==0.3.1`
- `msrest==0.6.21`
- `msrestazure==0.6.4`
- `oauthlib==3.1.1`
- `portalocker==2.3.2`
- `pycparser==2.21`
- `PyJWT==2.3.0`
- `pyodbc==4.0.32`
- `python-dateutil==2.8.2`
- `python-dotenv==0.19.2`
- `pywin32==303`
- `requests==2.27.1`
- `requests-oauthlib==1.3.0`
- `six==1.16.0`
- `tqdm==4.62.3`
- `urllib3==1.26.8`

The list of dependencies is to be found at [requirements.txt](https://github.com/virbickt/aruodas-rent-price-predictions/blob/main/requirements.txt)

## License
The project is licenced under [MIT License](https://github.com/virbickt/tlc-data-pipeline/blob/main/LICENSE.md)

## Contact
[tvirbickas@gmail.com](mailto:tvirbickas@gmail.com?subject=tlc-data-pipeline%20on%20Github)
