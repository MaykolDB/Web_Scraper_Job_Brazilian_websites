# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 16:13:53 2021

@author: Maykol
"""

import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import csv
import random
import re
import pandas as pd

def Get_user_agent():
    file= open('user-agents.txt','r')
    ua_strings= file.readlines()
    file.close()
    ua_strings= [x.strip() for x in ua_strings]
    return random.choice(ua_strings)

def Get_html(url):
    global soup, page
    page= url
    headers = {'User-Agent': Get_user_agent()}
    content = None
 
    try:
        response = requests.get(url, headers=headers)
        ct = response.headers['Content-Type'].lower().strip()
 
        if 'text/html' in ct:
            content = response.content
            soup = BeautifulSoup(content, "html.parser")
        else:
            content = response.content
            soup = None
        return soup
    
    except Exception as e:
        print("Error: " +str(url))

def Get_html_trabalhaBrasil():
    global html_trabalhaBrasil
    driver= webdriver.Chrome(executable_path="chromedriver.exe")
    url= 'https://www.trabalhabrasil.com.br/'
    driver.get(url)
    search_city= driver.find_element_by_xpath('//*[@id="txtCityQuery"]')
    search_city.click()
    search_city.send_keys('Curitiba')
    time.sleep(1)
    search_city.send_keys(Keys.ENTER)
    seek_vacancy= driver.find_element_by_xpath('//*[@id="btnBuscarVagas"]')
    time.sleep(1)
    seek_vacancy.click()
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(5)
    html_trabalhaBrasil = driver.page_source
    driver.close()
    
Get_html_trabalhaBrasil()

def Get_url_trabalhaBrasil():
    csv_file= open("Desc_url_vac_trabalhaBrasil.csv", "w", encoding= "utf-8")
    csv_write= csv.writer(csv_file)
    csv_write.writerow(['Title','Company','Salary','City_State','Description','Date','Link'])
    soup= BeautifulSoup(html_trabalhaBrasil, 'html.parser')
    for elem in soup.find_all('div', 'job__container'):
        Date= "not found"
        try:
            Title= elem.find(class_="job-vacancy-occupation").text.strip()
        except AttributeError:
             Title= "not found"
        try:
            Company= elem.h4.text
        except AttributeError:
            Company= "not found"
        try:
            Salary= elem.find(class_="job-vacancy-salary").text.split(" -")[0]
        except AttributeError:
            Salary= "not found"
        try:
            Description= elem.find(class_="job-vacancy-description").text.strip()
        except AttributeError:
            Description= "not found"
        try:
            City_State= elem.find(class_="job-vacancy-salary").text.split("- ")[1].strip()
        except AttributeError:
            City_State= "not found"
        except IndexError:
            City_State= "not found"
        try:
            Link= "https://www.trabalhabrasil.com.br"+elem.a.get('href')
        except AttributeError:
            Link= "not found"
        csv_write.writerow([Title,Company,Salary,City_State,Description,Date,Link])
    csv_file.close()
    
Get_url_trabalhaBrasil()

def Get_data_trabalhaBrasil():
    desc_trabalhaBrasil= pd.read_csv("Desc_url_vac_trabalhaBrasil.csv", sep=',', encoding="utf-8")
    
    csv_file= open("Desc_vac_trabalhaBrasil.csv", "w", encoding= "utf-8")
    csv_write= csv.writer(csv_file)
    csv_write.writerow(['Title','Company','Salary','City_State','Description','Date','Link'])
    count = 0
    A= Get_html(desc_trabalhaBrasil.Link[count ])
    B= Get_html(desc_trabalhaBrasil.Link[count +1])
    C= Get_html(desc_trabalhaBrasil.Link[count +2])
    D= Get_html(desc_trabalhaBrasil.Link[count +3])
    A_1= A.find('div', class_="col-md-3 remove__padding text-center").text.strip()
    B_1= B.find('div', class_="col-md-3 remove__padding text-center").text.strip()
    C_1= C.find('div', class_="col-md-3 remove__padding text-center").text.strip()
    D_1= D.find('div', class_="col-md-3 remove__padding text-center").text.strip()

    while A_1=='Publicada hoje' or B_1=='Publicada hoje' or C_1=='Publicada hoje' or D_1 =='Publicada hoje':
        
        soup= Get_html(desc_trabalhaBrasil.Link[count ])

        try:
            Date= soup.find('div', class_="col-md-3 remove__padding text-center").text.strip()
            Title= soup.find('h1', class_="job-title").text.strip().split(' em ')[0]
            Company= desc_trabalhaBrasil.Company[count ]
            Salary= desc_trabalhaBrasil.Salary[count ]
            Description= soup.find('p', class_="job-plain-text").text.strip()
            City_State= desc_trabalhaBrasil.City_State[count ]
            Link= desc_trabalhaBrasil.Link[count ]
            csv_write.writerow([Title,Company,Salary,City_State,Description,Date,Link])

        except AttributeError:
            Date= desc_trabalhaBrasil.Date[count ]
            Title= desc_trabalhaBrasil.Title[count ]
            Company= desc_trabalhaBrasil.Company[count ]
            Salary= desc_trabalhaBrasil.Salary[count ]
            Description= desc_trabalhaBrasil.Description[count ]
            City_State= desc_trabalhaBrasil.City_State[count ]
            Link= desc_trabalhaBrasil.Link[count ]
            csv_write.writerow([Title,Company,Salary,City_State,Description,Date,Link])
        count +=1
        print(count )
        A= Get_html(desc_trabalhaBrasil.Link[count +1])
        B= Get_html(desc_trabalhaBrasil.Link[count +2])
        C= Get_html(desc_trabalhaBrasil.Link[count +3])
        D= Get_html(desc_trabalhaBrasil.Link[count +4])
        A_1= A.find('div', class_="col-md-3 remove__padding text-center").text.strip()
        B_1= B.find('div', class_="col-md-3 remove__padding text-center").text.strip()
        C_1= C.find('div', class_="col-md-3 remove__padding text-center").text.strip()
        D_1= D.find('div', class_="col-md-3 remove__padding text-center").text.strip()

    csv_file.close()

Get_data_trabalhaBrasil()

def Get_url_vagascertas():
    csv_file= open("Desc_url_vac_vagascertas.csv", "w", encoding= "utf-8")
    csv_write= csv.writer(csv_file)
    csv_write.writerow(['Title','Company','Salary','City_State','Description','Date','Link'])
    soup= Get_html('https://www.vagascertas.com/vagas/vagas/1')
    elems= soup.find_all('article', "box vaga")
    elem= elems[1]
    date_n= elem.find('span', class_="m_bottom ds_inblock").text.split(" ")[2]
    date_now = datetime.now().strftime("%d/%m/%Y")
    count = 1
    while  date_n >= date_now:

        soup= Get_html('https://www.vagascertas.com/vagas/vagas/%i' % (count ))
        for elem in soup.find_all('article', "box vaga"):
            Company= "not found"
            try:
                Title= elem.h2.text
            except AttributeError:
                Title= "not found"
            try:
                Salary= elem.find('span', class_="m_top").text.split(': ')[1]
            except AttributeError:
                Salary= "not found"
            try:
                Description= elem.find("p", class_="m_top").text
            except AttributeError:
                Description= "not found"
            try:
                City_State= elem.find('span', class_="ds_inblock m_top").text
            except AttributeError:
                City_State= "not found"
            try:
                Date= elem.find('span', class_="m_bottom ds_inblock").text.split(" ")[2]
            except AttributeError:
                Date= "not found"
            try:
                Link= elem.a.get('href')
            except AttributeError:
                Link: "not found"
            csv_write.writerow([Title,Company,Salary,City_State,Description,Date,Link])
        date_n= Date
        count +=1

    csv_file.close()

Get_url_vagascertas()

def Get_data_vagascertas():
    data_vagas_vagascertas= pd.read_csv("Desc_url_vac_vagascertas.csv", sep=',', encoding="utf-8")
    data_vagas_vagascertas_Curitiba= data_vagas_vagascertas[data_vagas_vagascertas['City_State']==' Curitiba - Paraná']
    data_vagascertas_filter_today= data_vagas_vagascertas_Curitiba.reset_index()
    del data_vagascertas_filter_today['index']
    data_vagascertas_filter_today.to_csv("Desc_vac_vagascertas.csv")
    
Get_data_vagascertas()

def Get_url_indeed():

    csv_file= open("Desc_url_vac_indeed.csv", "w", encoding= "utf-8")
    csv_write= csv.writer(csv_file)
    csv_write.writerow(['Title','Company','Salary','City_State','Description','Date','Link'])
    soup= Get_html('https://br.indeed.com/jobs?l=Curitiba,+PR&rbl=Curitiba,+PR&jlid=6380af2affbafac7&fromage=1&start=0')
    temp_string = soup.title.text
    n = [int(temp)for temp in temp_string.split() if temp.isdigit()]
    if len(n)== 0:
        print("error: " + temp_string)
        
    else:
        count = 0
        while count  < n[0]:
            delay = random.randint(1, 3)
            sleep(delay)
            soup= Get_html('https://br.indeed.com/jobs?l=Curitiba,+PR&rbl=Curitiba,+PR&jlid=6380af2affbafac7&fromage=1&start=%i' % (count ))
            for elem in soup.find_all('div', 'jobsearch-SerpJobCard'):
                try:
                    Title= elem.h2.a.get('title').strip()
                except AttributeError:
                    Title= "not found"
                try:
                    Company= elem.find('span', 'company').text.strip()
                except AttributeError:
                    Company= "not found"
                try:
                    Salary= elem.find('span', 'salaryText').text.strip()
                except AttributeError:
                    Salary= "not found"
                try:
                    Description= elem.find('div', "summary").text.strip()
                except AttributeError:
                    Description= "not found"
                try:
                    City_State= elem.find('div', "recJobLoc").get('data-rc-loc').strip()
                except AttributeError:
                    City_State= "not found"
                try:
                    Date= elem.find('span', "date").text.strip()
                except AttributeError:
                    Date= "not found"
                try:
                    Link= 'https://br.indeed.com'+elem.h2.a.get('href')
                except AttributeError:
                    Link= "not found"
                csv_write.writerow([Title,Company,Salary,City_State,Description,Date,Link])
            
            count +=10
        csv_file.close()

Get_url_indeed()

def Get_data_indeed():
    data_vac_indeed= pd.read_csv("Desc_url_vac_indeed.csv", sep=',', encoding="utf-8")
    Desc_vac_indeed_hoje= data_vac_indeed[data_vac_indeed['Date']!='há 1 dia']
    Desc_vac_indeed_hoje= Desc_vac_indeed_hoje.reset_index()
    del Desc_vac_indeed_hoje['index']
    Desc_vac_indeed_hoje.to_csv("Desc_vac_indeed.csv")
    
Get_data_indeed()

def Get_url_contratoimediato():
    csv_file= open("Desc_url_vac_contratoimediato.csv", "w", encoding= "utf-8")
    csv_write= csv.writer(csv_file)
    csv_write.writerow(['Title','Company','Salary','City_State','Description','Date','Link'])
    soup= Get_html('https://www.contratoimediato.com/')
    elems= soup.find_all('div', 'post-outer')
    elem= elems[0]
    date_n= elem.find('abbr', class_="published updated").get('title').split('T')[0]
    date_n= datetime.strptime(date_n, '%Y-%m-%d')
    date_n= datetime.strftime(date_n,"%d/%m/%Y")
    date_now = datetime.now().strftime("%d/%m/%Y")
    count = 0
    while  date_n <= date_now:
        if count  == 0:
            soup= Get_html('https://www.contratoimediato.com/')
            count = 1
        else:
            soup= Get_html(f'https://www.contratoimediato.com/search?updated-max=2021-03-22T11%3A08%3A00-03%3A00&max-results=8#PageNo={count }')
        for elem in soup.find_all('div', 'post-outer'):
            Company= "not found"
            try:
                Title= elem.h2.a.get('title').strip()
            except AttributeError:
                Title= "not found"
            try:
                Salary= "not found"
            except AttributeError:
                Salary= "not found"
            try:
                Description= "not found"
            except AttributeError:
                Description= "not found"
            try:
                City_State= "not found"
            except AttributeError:
                City_State= "not found"
            try:
                Date= elem.find('abbr', class_="published updated").get('title').split('T')[0]
                Date= datetime.strptime(Date, '%Y-%m-%d')
                Date= datetime.strftime(Date,"%d/%m/%Y")
            except AttributeError:
                Date= "not found"
            try:
                Link= elem.h2.a.get('href')
            except AttributeError:
                Link: "not found"
            csv_write.writerow([Title,Company,Salary,City_State,Description,Date,Link])
        date_n= Date
        count +=1

    csv_file.close()

Get_url_contratoimediato()

def Get_data_contratoimediato():
    Desc_url_vac_contratoimediato= pd.read_csv("Desc_url_vac_contratoimediato.csv", sep=',', encoding="utf-8")
    
    csv_file= open("Desc_vac_contratoimediato.csv", "w", encoding= "utf-8")
    csv_write= csv.writer(csv_file)
    csv_write.writerow(['Title','Company','Salary','City_State','Description','Date','Link'])
    count = 0
    while count  < Desc_url_vac_contratoimediato.shape[0]:
        Date= Desc_url_vac_contratoimediato.Date[count ]
        Company= Desc_url_vac_contratoimediato.Company[count ]
        Salary= Desc_url_vac_contratoimediato.Salary[count ]
        City_State= Desc_url_vac_contratoimediato.City_State[count ]
        Link= Desc_url_vac_contratoimediato.Link[count ]
        soup= Get_html(Desc_url_vac_contratoimediato.Link[count ])
        elem= soup.find_all('div', id="adsense-target")
        try:
            Title= elem.find('div').next.next.split('Vagas de emprego: ')[1]
        except AttributeError:
            Title= Desc_url_vac_contratoimediato.Title[count ]
        try:
            Description= elem[0].text
        except:
            Description= Desc_url_vac_contratoimediato.Description[count ]
       
        csv_write.writerow([Title,Company,Salary,City_State,Description,Date,Link])
        count +=1 

    csv_file.close()

Get_data_contratoimediato()

def  Data_today():
    data_trabalhaBrasil_filter_today= pd.read_csv("Desc_vac_trabalhaBrasil.csv", sep=',', encoding="utf-8")
    data_vagascertas_filter_today= pd.read_csv("Desc_vac_vagascertas.csv", sep=',', encoding="utf-8")
    data_indeed_filter_today= pd.read_csv("Desc_vac_indeed.csv", sep=',', encoding="utf-8")
    data_contratoinmediato_filter_today= pd.read_csv("Desc_vac_contratoimediato.csv", sep=',', encoding="utf-8")
    data_desc_vac= pd.concat([data_trabalhaBrasil_filter_today, data_vagascertas_filter_today, data_indeed_filter_today,data_contratoinmediato_filter_today])
    data_desc_vac= data_desc_vac.reset_index()
    del data_desc_vac['index']
    word_list= pd.read_csv("word_list_filter_vac.csv", sep=';', encoding="utf-8", index_col=0)
    csv_file= open("data.csv", "w", encoding= "utf-8")
    csv_write= csv.writer(csv_file)
    csv_write.writerow(['Title','Company','Salary','City_State','Description','Date','Link'])
    i= 0 #pattern/word
    j= 0 #flags/texto
    while i < (word_list.Word.shape[0]-1):
        while j < (data_desc_vac.shape[0]-1):
            flags=  data_desc_vac.Description[j]
            pattern= word_list.Word[i]
            if re.search(pattern, flags, re.IGNORECASE):
                Title= data_desc_vac.Title[j]
                Company= data_desc_vac.Company[j]
                Salary= data_desc_vac.Salary[j]
                Description= data_desc_vac.Description[j]
                City_State= data_desc_vac.City_State[j]
                Date= data_desc_vac.Date[j]
                Link= data_desc_vac.Link[j]
                csv_write.writerow([Title,Company,Salary,City_State,Description,Date,Link])
                break 
            j+= 1
        i+= 1
        j=0
    i= 0 #pattern/word
    j= 0 #flags/texto
    while i < (word_list.Word.shape[0]-1):
        while j < (data_desc_vac.shape[0]-1):
            flags2= data_desc_vac.Title[j]
            pattern= word_list.Word[i]
            if re.search(pattern, flags2, re.IGNORECASE):
                Title= data_desc_vac.Title[j]
                Company= data_desc_vac.Company[j]
                Salary= data_desc_vac.Salary[j]
                Description= data_desc_vac.Description[j]
                City_State= data_desc_vac.City_State[j]
                Date= data_desc_vac.Date[j]
                Link= data_desc_vac.Link[j]
                csv_write.writerow([Title,Company,Salary,City_State,Description,Date,Link])
                break 
            j+= 1
        i+= 1
        j=0

    csv_file.close()
    
Data_today()

def Send_msg():
    global data
    data= pd.read_csv("data.csv", sep=',', encoding="utf-8")
    data= data.drop_duplicates()
    data= data.reset_index()
    del data['index']
    no_of_message= 1 # no. of time 
    moblie_no_list=[554199999999] # list of phone number 

    def element_presence(by,xpath,time):
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, time).until(element_present)

    driver = webdriver.Chrome(executable_path= "chromedriver.exe")
    driver.get("http://web.whatsapp.com")
    sleep(10) #wait time to scan the code in second


    for moblie_no in moblie_no_list:
        driver.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(moblie_no))
        try:
            driver.switch_to_alert().accept()
        except Exception as e:
                pass
        count = 0
        while count  < data.shape[0]:
            message_text= data.Link[count ]
            try:
                element_presence(By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]',30)
                txt_box=driver.find_element(By.XPATH , '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
                for x in range(no_of_message):
                    txt_box.send_keys(message_text)
                    sleep(5)
                    txt_box.send_keys("\n")
            except Exception as e:
                print("invailid phone no : "+str(moblie_no))
            print(str (count +1)+" Sent messages")
            count +=1

Send_msg()













