import requests
import statistics
import regex as re
import pandas as pd
from bs4 import BeautifulSoup
from pandas.core.interchange.dataframe_protocol import DataFrame


class DataManager:
    def __init__(self, url="https://aijobs.net/?cou=78&key=&exp=&sal="):
        # Default url contains ai jobs applications located in France
        self.URL = url
        self.URL_PREFIX = re.findall('https:\/\/[^\/]+\/', url)[0]
        self.data_df = pd.DataFrame()


    def get_data(self):
        return self.data_df


    def fetch_page_data(self, url):
        print(f"Fetching data from : {self.URL_PREFIX}{url}")
        page = requests.get(f"{self.URL_PREFIX}{url}")
        soup = BeautifulSoup(page.content, 'html.parser')
        job_text_wrapper = soup.css.select_one('.container-xl > .row > .col-md-10')

        job_params = {
            "job_link": f"{self.URL_PREFIX}{url}",
            "job_title": None,
            "job_company": None,
            "job_location": None,
            "job_contract": None,
            "job_level": None,
            "job_salary": None,
            "job_salary_mean": None,
            "job_tags": None,
            "job_perks_and_benefits": None,
        }

        job_title = soup.find('h1', class_='display-5 mt-4 text-break')
        job_company = soup.find('h2', class_='h5')
        job_location = soup.find('h3', class_='lead py-3')

        job_characteristics = soup.find('h5', class_='pb-2')
        job_contract = job_characteristics.find_all('span', class_='text-bg-secondary')
        job_level = job_characteristics.find('span', class_='text-bg-info')
        job_salary = job_characteristics.find('span', class_='text-bg-success')

        job_p_direct_children = job_text_wrapper.find_all('p', recursive=False)

        if job_title is not None:
            job_params["job_title"] = job_title.string

        if job_company is not None:
            job_params["job_company"] = job_company.string

        if job_location is not None:
            job_params["job_location"] = job_location.string

        if job_contract is not None:
            contracts = []
            for contract in job_contract:
                contracts.append(contract.string)

            job_params["job_contract"] = ';'.join(contracts)

        if job_level is not None:
            job_params["job_level"] = job_level.string

        if job_salary is not None:
            job_params["job_salary"] = job_salary.contents[0].string
            job_mean = re.findall('\d+', job_params["job_salary"])
            job_mean = map(int, job_mean)
            job_mean = statistics.mean(job_mean)
            job_params["job_salary_mean"] = job_mean

        if job_p_direct_children is not None:
            for p in job_p_direct_children:
                if len(p.contents) > 1:
                    if re.search('Tags:', p.contents[0].string):
                        job_tags = []
                        tags = p.contents[1].find_all('span', class_='badge rounded-pill text-bg-light')

                        for tag in tags:
                            job_tags.append(tag.a.string)

                        job_params["job_tags"] = ';'.join(job_tags)

                    if re.search('Perks/benefits:', p.contents[0].string):
                        job_perks_and_benef = []
                        tags = p.contents[1].find_all('span', class_='badge rounded-pill text-bg-light')

                        for tag in tags:
                            job_perks_and_benef.append(tag.a.string)

                        job_params["job_perks_and_benefits"] = ';'.join(job_perks_and_benef)

        return pd.DataFrame(job_params, index=[0])


    def fetch_site_data(self):
        print(f"Started fetching data from : {self.URL}")
        page = requests.get(self.URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        print(f"Finished fetching data from : {self.URL}")

        results = soup.find_all('li', class_='list-group-item')
        for result in results:
            page_a = result.find('a', class_='col py-2')

            if page_a is not None:
                page_link = page_a['href'][1:] # [1:] removes the / at the start of the url
                page_data = self.fetch_page_data(page_link)
                page_data = pd.DataFrame(page_data)

                if not page_data.empty:
                    self.data_df = pd.concat([self.data_df, page_data], ignore_index=True)


    def fetch_api_data(self, url=''):
        pass


    def get_csv_data(self, url='data/raw/data.csv'):
        csv_file = pd.read_csv(url)
        return csv_file


    def save_data_to_csv(self, path='data/raw/data.csv'):
        newDf = pd.DataFrame(self.get_data())

        pd.DataFrame.to_csv(newDf, path, index=False)
