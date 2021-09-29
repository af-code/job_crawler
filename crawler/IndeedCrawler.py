import requests
from bs4 import BeautifulSoup

class IndeedCrawler:

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'}

    def recieve_indeed_job(self, url):
        source = requests.get(url, headers=self.headers).text.encode('utf-8')
        soup = BeautifulSoup(source, 'html.parser') 
        try:
            content = soup.find("div", {"class": 'jobsearch-JobComponent-description icl-u-xs-mt--md'}).text
        except AttributeError:
            content = 'Error'

        return content

    def indeed_job_list(self, url):
        source = requests.get(url, headers=self.headers).text.encode('utf-8')
        soup = BeautifulSoup(source, 'html.parser')
        job_list = []
        try:
            temp = soup.find_all("a", {"data-hide-spinner": "true"})
            extraUrl = 'https://de.indeed.com'
            for i in temp:
                job_list.append(extraUrl + i.attrs["href"])
        except AttributeError:
            job_list = []
        return job_list

if __name__ == '__main__':
    indeed_crawler = IndeedCrawler()
    url = 'https://de.indeed.com/jobs?q=Softwareentwickler&l=Siegen&radius=100'
    for i in indeed_crawler.indeed_job_list(url):
        print(indeed_crawler.recieve_indeed_job(i))