# selenium==4.9.1
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from w3lib.html import remove_tags


class census():

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        self.driver.get("https://www.census2011.co.in/census/state/districtlist/maharashtra.html")


    def taluka_links(self,district_links):
        taluka_links = []
        m = 0  # baad me nikal do
        for i,j in district_links:
            self.driver.get(j)
            taluka_name_and_links = self.driver.find_elements(By.XPATH,'//table[@class="table table-striped table-hover "]/tbody/tr/td[2]/a')
            if m == 2:
                break
            for k in taluka_name_and_links:

                taluka_links.append((i,k.get_attribute("innerHTML"),k.get_attribute("href")))
                print(i,k.get_attribute("innerHTML"),k.get_attribute("href"))
            m += 1
        return taluka_links

    def find_taluka_villages_links(self,taluka_links):
        taluka_village_links = []
        m = 0  # baad me nikal do
        for i,j,k in taluka_links:
            self.driver.get(k)
            taluka_village_name_links = self.driver.find_elements(By.XPATH,'//div[@class="table-responsive"][2]/table[@class="table table-striped table-hover "][1]/tbody/tr/td[2]/a')
            if m == 2:
                break
            # i = district
            # j = taluka
            # k = taluka link
            for l in taluka_village_name_links:
                taluka_village_links.append((i,j,l.get_attribute("innerHTML"),l.get_attribute("href")))
                print(i,j,l.get_attribute("innerHTML"),l.get_attribute("href"))

            m += 1
        return taluka_village_links


    def find_village_data(self,taluka_village_links):
        data = pd.DataFrame(columns=["District","Taluka","Village",'total_no_of_houses',"population","population_male","population_female","child","child_male","child_female","schedule_cast","schedule_cast_male",
                                     "schedule_caste_female","schedule_tirbe","schedule_tribe_male","schedule_tribe_female","literacy"
                                     ,"literacy_male","literacy_female","total_workers","total_workers_male","total_workers_female","main_worker","main_worker_male","main_worker_female",
                                     "marginal_workers","marginal_workers_male","marginal_workers_female"])
        cols = ['District','Taluka','Village','total_no_of_houses',"population","population_male","population_female","child","child_male","schedule_cast","schedule_cast_male",
                                     "schedule_caste_female","schedule_tirbe","schedule_tribe_male","schedule_tribe_female","literacy"
                                     ,"literacy_male","literacy_female","total_workers","total_workers_male","total_workers_female","main_worker","main_worker_male","main_worker_female",
                                     "marginal_workers","marginal_workers_male","marginal_workers_female"]

        # l = district
        # m = taluka
        # n = village
        # o = village link
        for l,m,n,o in taluka_village_links:
            self.driver.get(o)
            table_data = self.driver.find_elements(By.XPATH, '//div[@id="column3"]/table/tbody/tr/td')
            row = [l,m,n]
            for i in range(0, len(table_data)):
                if i % 4 != 0:
                    row.append(remove_tags(table_data[i].get_attribute("innerHTML")).strip())
            row.pop(4)
            row.pop(4)
            print(len(cols),len(row),row)
            data.loc[data.shape[0]] = row
        print(data)
        data.to_csv("data1.csv")
        return data


    def find_main_city_links(self):
        main_district_links = self.driver.find_elements(By.XPATH,'//div[@class="col-sm-8"]/table/tbody/tr/td[2]/a')
        main_subdistrict_links = self.driver.find_elements(By.XPATH,'//div[@class="col-sm-8"]/table/tbody/tr/td[3]/a')
        district_links = []
        for i,j in zip(main_district_links,main_subdistrict_links):
            district_links.append((i.get_attribute("innerHTML"),j.get_attribute("href")))
            print(i.get_attribute("innerHTML"),j.get_attribute("href"))
        return district_links


if __name__ == "__main__":
    data = census()
    district_links = data.find_main_city_links()
    taluka_links = data.taluka_links(district_links)
    taluka_village_links = data.find_taluka_villages_links(taluka_links)
    #temp_links = ['https://www.census2011.co.in/data/village/552457-bale-maharashtra.html','https://www.census2011.co.in/data/village/556029-akurdi-maharashtra.html']
    data.find_village_data(taluka_village_links)
