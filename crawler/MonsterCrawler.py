import requests
from bs4 import BeautifulSoup


class MonsterCrawler:

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'}

    def monster_job_list(self, url):
        source = requests.get(url, headers=self.headers).text.encode('utf-8')
        soup = BeautifulSoup(source, 'html.parser')
        job_list = []
        try:
            temp = soup.find_all("div", {"class": "title-company-location"})
            temp_list = []
            for i in temp:
                temp_list.append(i.find("a"))

            for i in temp_list:
                job_list.append(i.attrs["href"])
        except AttributeError:
            job_list = []

        return job_list

    def recieve_monster_job(self, url):
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')

        try:
            content = soup.find("div", {"class": "job-description"}).text
        except AttributeError:
            content = 'Error'

        return content
