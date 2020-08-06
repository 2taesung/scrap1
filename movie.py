import requests
from bs4 import BeautifulSoup
import csv


base_url = 'https://movie.naver.com/movie/running/current.nhn'

URL = base_url

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')


movie_section = soup.select(
    '#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li' )

movie_datas = []
for movie in movie_section:
    title_tag = movie.select_one('div > a > img')
    code_tag = movie.select_one('div > a')

    movie_title = title_tag['alt']
    movie_code = code_tag['href']
    movie_code_list = movie_code.split('=')

    # print(movie_title)
    # print(movie_code_list[1], '\n')

    movie_data = {
        'title' : movie_title,
        'code' : movie_code_list[1]
    }
    movie_datas.append(movie_data)
    # with open('./movies.csv', 'a') as csvfile:
    #     fieldnames = ['title', 'code']
    #     csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     csvwriter.writerow(movie_data)

# print(movie_datas)

for movie in movie_datas:
    movie_code = movie['code']

    REVIEW_URL = r'https://movie.naver.com/movie/bi/mi/basic.nhn?code={movie_code}'

    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    review_section = soup.select(
        'body > div > div > div.score_result > ul > li' )
    
    count = 0
    for review in review_section:
        score = review.select_one('.star_score > em').text

        if review.select_one(f'.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}') is None:
            review = review.select_one(f'.score_reple > p > span#_filtered_ment_{count}').text.strip()
        elif review.select_one(f'.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}'):
            review = review.select_one(f'.score_reple > p > span#_filtered_ment_{count} > span > a')['data-src']


        print("평점 : ", score, "\n리뷰 : ", review, "\n")

        count += 1