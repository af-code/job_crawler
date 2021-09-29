import requests
from bs4 import BeautifulSoup
from time import sleep

class StepstoneCrawler:

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'}

    def stepstone_job_list(self, url):
        source = requests.get(url, headers = self.headers).text
        soup = BeautifulSoup(source, 'html.parser')
        job_list = []
        try:
            temp = soup.find_all("div", {"class": "sc-fzpisO dikqXf"})
            temp_list = []
            for i in temp:
                temp_list.append(i.find("a", {"class": "sc-fzoiQi eRNcm"}))

            for i in temp_list:
                job_list.append(i.attrs["href"])
        except AttributeError:
            job_list = []
        return job_list

    def recieve_stepstone_job(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Referer': 'https://google.com', 
        }
        try:
            source = requests.get(url, headers=headers).text
        except requests.exceptions.ConnectionError:
            sleep(2.5)
            self.recieve_stepstone_job(url)
        soup = BeautifulSoup(source, 'html.parser')
        try:
            content = soup.find("div", {"class": "js-app-ld-ContentBlock"}).text
        except AttributeError:
            content = 'Error'
        return content
    
if __name__ == '__main__':
    url = 'https://www.stepstone.de/stellenangebote--Junior-Softwareentwickler-Schwerpunkt-Backend-Entwicklung-NET-m-w-d-Siegen-statmath-GmbH--7369799-inline.html?rltr=1_1_4_hc_re_0_0_0_0_0_0'
    stepstone_crawler = StepstoneCrawler()
    print(stepstone_crawler.recieve_stepstone_job(url))