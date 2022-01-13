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
Application has no interface and is only suitable for sending the input values and receiving predictions in json format using either Python's in-built `requests` or, Postman.
API consists in two routes:
#### generate_urls
- `generate_urls()`
Generates a list of urls to collect the data from by iterating over the range of years that the `Collector` object has been inicialized with. If the number for the month consists in a single digit, it is appended with `0`.

    Returns (List[str]): list that contains urls for each month's data in `.csv` format
#### extract_data
- `extract_data(url, filename)`
Retrieves the content of the page which are then written into a `.csv` file which is saved by the name specified as `filename`.

    Parameters:
    - url(str): the url to retrieve the content from and write into a .csv file.
    - file_name(str): the name which is to be used to save the file with.

    Returns: None


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
