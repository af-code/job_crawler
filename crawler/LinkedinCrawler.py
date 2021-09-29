import requests
from bs4 import BeautifulSoup

class LinkedinCrawler:

    def linkedin_job_list(self, url):
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')
        job_list = []
        try:
            temp = soup.find_all("a", {"class": "base-card__full-link"})
            for i in temp:
                try:
                    job_list.append(i.attrs["href"])
                except KeyError:
                    continue
        except AttributeError:
            job_list = []

        return job_list
    
    def recieve_linkedin_job(self, url):
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')

        try:
            content = soup.find("section", {"class": "description"}).text
        except AttributeError:
            content = 'Error'

        return content.replace('Mehr anzeigen', '').replace('Weniger anzeigen', '')