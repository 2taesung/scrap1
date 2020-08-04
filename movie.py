import requests
from bs4 import BeautifulSoup
import csv


base_url = 'https://movie.naver.com/movie/running/current.nhn'

URL = base_url

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')


movie_section = soup.select(
    '#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li' )

for movie in movie_section:
    title_tag = movie.select_one('div > a > img')
    code_tag = movie.select_one('div > a')

    movie_title = title_tag['alt']
    movie_code = code_tag['href']
    movie_code_list = movie_code.split('=')

    # print(movie_title)
    # print(movie_code_list[1], '\n')

    news_data = {
        'title' : movie_title,
        'code' : movie_code_list[1]
    }

    with open('./movies.csv', 'a') as csvfile:
        fieldnames = ['title', 'code']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writerow(news_data)
