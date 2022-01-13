import os
import shutil
from typing import List

import humanize
import requests


class Collector:
    def __init__(self, start_year: int = 2009, end_year: int = 2021) -> None:
        self.start_year = start_year
        self.end_year = end_year

    def generate_urls(self) -> List[str]:
        """
        Generate a list of urls to collect the data from by iterating over the range of years that the Collector object has been inicialized with. If the number for the month consists in a single digit, it is appended with 0.

        :return: list that contains urls for each month's data in csv format
        :rtype: List[str]
        """
        urls = []
        for i in range(self.start_year, self.end_year + 1, 1):
            base_url = (
                f"https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_{i}-"
            )
            if i == 2021:
                year_urls = [f"{base_url}0{month}.csv" for month in range(1, 8)]
            else:
                year_urls = [
                    f"{base_url}0{month}.csv"
                    if month in range(1, 10)
                    else f"{base_url}{month}.csv"
                    for month in range(1, 13)
                ]
            urls.extend(year_urls)
        return urls

    def extract_data(
        self,
        url: str = "https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-07.csv",
        file_name: str = "2021-07.csv",
    ) -> None:
        """
        Iterates over the generated urls to get the content of each page which are then written into a csv file.

        :return: None
        :rtype: NoneType
        """

        print(f"\nSending a request for {file_name}")
        with requests.get(url, stream=True) as r:
            with open(file_name, "wb") as f:
                print(f"Saving the contents as {file_name}")
                shutil.copyfileobj(r.raw, f)

        file_size = os.path.getsize(file_name)
        print(
            f"{file_name} has been successfully saved. File size: {humanize.naturalsize(file_size)}"
        )
