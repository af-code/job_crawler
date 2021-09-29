from crawler.IndeedCrawler import IndeedCrawler
from crawler.MonsterCrawler import MonsterCrawler
from crawler.LinkedinCrawler import LinkedinCrawler
from crawler.StepstoneCrawler import StepstoneCrawler
from DatabaseConnector import DatabaseConnector

indeed_crawler = IndeedCrawler()
monster_crawler = MonsterCrawler()
linkedin_crawler = LinkedinCrawler()
stepstone_crawler = StepstoneCrawler()
databaseConnector = DatabaseConnector()

class MainCrawler():

    def start_crawler(self, site: str, job: str, city: str, radius: str):
        if(site == "indeed"):
            self.__indeed(job, city, radius)
        
        if(site == "monster"):
            self.__monster(job, city, radius)
        
        if(site == "linkedIn"): 
            self.__linkedIn(job, city, radius)
        
        if(site == "stepstone"):
            self.__stepstone(job, city, radius)
    
    def __indeed(self, job: str, city: str, radius):
        indeed_link = 'https://de.indeed.com/jobs?q='+job+'&l='+city+'&radius='+radius
        side_array = ['', '&start=10', '&start=20', '&start=30', '&start=40', '&start=50']
        for i in side_array:
            index = indeed_link.find("&start")
            if index >= 0:
                indeed_link = indeed_link[:index] + i

            for j in indeed_crawler.indeed_job_list(indeed_link):
                if 'pagead' not in j:
                    databaseConnector.insert_in_table('Indeed', j, job, city, radius, indeed_crawler.recieve_indeed_job(j))
            indeed_link += '&start'

    def __monster(self, job: str, city: str, radius: str):
        monster_link_standard = 'https://www.monster.de/jobs/suche/?q='+job+'&where='+city+'&rd='+radius
        side_array = ['', '&page=2', '&page=3', '&page=4', '&page=5']
        for i in side_array:
            monster_link = monster_link_standard + i
            for j in monster_crawler.monster_job_list(monster_link):
                databaseConnector.insert_in_table('Monster', j, job, city, radius, monster_crawler.recieve_monster_job(j))

    def __linkedIn(self, job: str, city: str, radius):
        linkedin_link = 'https://de.linkedin.com/jobs/search?keywords='+job+'&location='+city+'&geoid=&trk=guest_homepage-basic_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
        for i in linkedin_crawler.linkedin_job_list(linkedin_link):
            databaseConnector.insert_in_table('LinkedIn', i[:(i.rfind("?"))], job, city, radius, linkedin_crawler.recieve_linkedin_job(i))

    def __stepstone(self, job: str, city: str, radius: str):
        stepstone_link = 'https://www.stepstone.de/5/ergebnisliste.html?stf=freeText&ns=1&qs=%5B%5D&companyID=0&cityID=0&sourceOfTheSearchField=homepagemex%3Ageneral&searchOrigin=Homepage_top-search&ke='+job+'%2Fin&ws='+city+'&ra='+radius+'&rsearch=1'
        stepstone_string = "https://www.stepstone.de"
        for i in stepstone_crawler.stepstone_job_list(stepstone_link):
            databaseConnector.insert_in_table('Stepstone', stepstone_string+i, job, city, radius, stepstone_crawler.recieve_stepstone_job(stepstone_string+i))