import requests
from bs4 import BeautifulSoup
name = input()
ITEMS = 50
URL = f'https://kstovo.hh.ru/search/vacancy?text={name}&area=66&items_on_page={ITEMS}'

headers = {
  'Host': 'hh.ru',
  'User-Agent':'Safari',
  'Accept':'*/*',
  'Accept-Encoding':'gzip, deflate, br',
  'Connection':'keep-alive'
}

def extract_max_page():
  hh_request = requests.get(URL, headers=headers)
  hh_soup=BeautifulSoup(hh_request.text,'html.parser')
  pages=[]
  paginator=hh_soup.find_all('span',{'class':'pager-item-not-in-short-range'})
  for page in paginator:
    pages.append(int(page.find('a').text))
  return pages[-1]

def extract_job(html):
  title=html.find('a').text
  link=html.find('a')['href']
  company=html.find('div',{'class':'vacancy-serp-item__meta-info-company'}).find('a').text
  company=company.strip()
  location = html.find('div',{'data-qa':'vacancy-serp__vacancy-address'}).text
  location=location.partition(',')[0]
  return {'title':title, 'company':company, 'location':location,'link':link}
  
def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f'Парсинг страницы {page}')
    result = requests.get(f'{URL}&page={page}',headers=headers)
    soup=BeautifulSoup(result.text,'html.parser')
    results = soup.find_all('div',{'class':'vacancy-serp-item'})
    for result in results:
      job=extract_job(result)
      jobs.append(job)
  return jobs
 
def get_jobs():
  max_page=extract_max_page()
  jobs = extract_jobs(max_page)
  return jobs