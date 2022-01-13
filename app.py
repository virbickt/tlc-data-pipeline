import os
from datetime import datetime

from dotenv import load_dotenv
from tqdm import tqdm

from collector.collector import Collector
from database_manager.database_manager import Database
from file_manager.file_manager import FileManager

load_dotenv()

AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")


def main():
    start_time = datetime.now()

    # # collect the urls
    collector = Collector(2021, 2021)
    urls = collector.generate_urls()

    # create a container inside the storage which has already been created
    fmanager = FileManager()
    fmanager.create_container("tlc-datax")

    # create a server, a database, connect the database to the storage and create a table to store the data
    dbmanager = Database(
        AZURE_SUBSCRIPTION_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID
    )
    dbmanager.create_server(server_name="tlc-data-serverx", group_name="tlc-data-rg")
    dbmanager.create_database(
        server_name="tlc-data-serverx", database_name="tlc-data-dbx"
    )
    dbmanager.whitelist_ip(server_name="tlc-data-serverx")
    dbmanager.encrypt_database(
        server_name="tlc-data-serverx", database_name="tlc-data-dbx"
    )
    dbmanager.create_credentials(
        server_name="tlc-data-serverx", database_name="tlc-data-dbx"
    )
    dbmanager.create_external_data_source(
        server_name="tlc-data-serverx",
        database_name="tlc-data-dbx",
        container_name="tlc-datax",
    )
    dbmanager.create_table(
        server_name="tlc-data-serverx",
        database_name="tlc-data-dbx",
        table_name="tlc_datax",
    )

    # get the data and load it to the container and transfer it the database
    for url in tqdm(urls[1:2]):
        file_name = url.split("_")[-1]
        collector.extract_data(url, file_name)
        fmanager.upload_file("tlc-datax", file_name)
        dbmanager.load_csv_to_db(
            server_name="tlc-data-serverx",
            database_name="tlc-data-dbx",
            table_name="tlc_datax",
            file_name=file_name,
        )

    end_time = datetime.now()
    print("Duration: {}".format(end_time - start_time))


if __name__ == "__main__":
    main()
