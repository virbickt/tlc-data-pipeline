import os

from azure.storage.blob import BlobServiceClient
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class FileManager:
    def __init__(self):
        self.__storage_connection_string = os.getenv("STORAGE_CONNECTION_STRING")
        self.container_name = ""

    def create_container(self, container_name: str = "unnamed") -> None:
        """
        Creates a new container inside Azure Storage.

        :param container_name str: the name for the container
        :returns: None
        :rtype: NoneType
        """
        self.container_name = container_name
        blob_service_client = BlobServiceClient.from_connection_string(
            self.__storage_connection_string
        )
        print(f"Creating a new container '{container_name}'...\n")
        container_client = blob_service_client.create_container(self.container_name)
        print(f"Container '{container_name}' created successfully.\n")

    def upload_file(
        self, container_name: str = "tlc-data2", file_name: str = "unnamed"
    ) -> None:
        """
        Uploads the file to Azure Storage as a blob. As it is referred to in Azure documentation, blobs are Azure-specific objects
        that can hold text or binary data, including images, documents, etc.

        :param file_name str: the name for the file (blob). This is the name that the file is going to be stored with in your storage account.
        :returns: None
        :rtype: NoneType
        """
        blob_service_client = BlobServiceClient.from_connection_string(
            self.__storage_connection_string
        )
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=file_name
        )
        print("\nUploading to Azure Storage as blob:\n\t" + file_name + "\n")

        with open(file_name, "rb") as data:
            blob_client.upload_blob(data)
        print(f"\n{file_name} has been successfully uploaded.\n")

