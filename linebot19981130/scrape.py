import urllib.request
from bs4 import BeautifulSoup
import datetime
import re
import calendar
import json
import requests

url = 'https://www.nishinippon.co.jp/nsp/category/baseball/npb/hawks/'
# ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'\
#      'AppleWebKit/537.36 (KHTML, like Gecko)'\
#      'Chrome/89.0.4389.90 Safari/537.36'

def get_news():
    req = urllib.request.Request(url)
    html = urllib.request.urlopen(req)
    soup = BeautifulSoup(html, "html.parser")

    # r = requests.get(target_url)
    # soup = BeautifulSoup(r.text, 'lxml')

    a_box = []
    url_box = []
    result = []
    dt_now = datetime.datetime.now()
    year = dt_now.year
    month = dt_now.month
    # print(month)
    pre_month = 0
    if month == 1:
        pre_month = 12
    else:
        pre_month = month - 1
    # print(pre_month)
    day = dt_now.day
    # print(day)
    pre_day = 0
    if day == 1:
        pre_day = calendar.monthrange(year, month - 1)[1]
    else:
        pre_day = day -1
    # print(pre_day)
    # print(twentyone_date_time)
    article_contents = soup.find_all('div', class_='c-articleList__content')
    article_dates = []
    for article_content in article_contents:
        article_date = article_content.find('span', class_='c-articleList__date')
        # print(article_date.text)
        if day == 1:
            if re.match('..:..', article_date.text) or re.match('.:..', article_date.text):
                article_dates.append(article_date.text)
            elif re.match(str(pre_month) + '/' + str(pre_day) + ' ' + '21:..', article_date.text) or re.match(
                    str(pre_month) + '/' + str(pre_day) + ' ' + '22:..', article_date.text) or re.match(
                    str(pre_month) + '/' + str(pre_day) + ' ' + '23:..', article_date.text):
                article_dates.append(article_date.text)
            else:
                break
        else:
            if re.match('..:..', article_date.text) or re.match('.:..', article_date.text):
                article_dates.append(article_date.text)
            elif re.match(str(month) + '/' + str(pre_day) + ' ' + '21:..', article_date.text) or re.match(
                    str(month) + '/' + str(pre_day) + ' ' + '22:..', article_date.text) or re.match(
                    str(month) + '/' + str(pre_day) + ' ' + '23:..', article_date.text):
                article_dates.append(article_date.text)
            else:
                break
    # print(article_dates)

    for i in range(len(article_dates)):
        h3 = article_contents[i].find('h3')
        a = h3.find('a')
        if a.text[-3:] == "New":
            a_text = a.text.rstrip("New")
        else:
            a_text = a.text
        a_box.append(a_text)
        url_box.append(a.get('href'))

    # print(a_box)
    # print((url_box))
    for i in range(len(a_box)):
        result.append(a_box[i] + "\n" + "https://www.nishinippon.co.jp/" + url_box[i] + "\n\n")
    result_ans = '\n'.join(result)

    # print(result)
    # print(result_ans)
    return result_ans
    # for i in range(len(a_box)):
    #     if a_box[i][-3:] == "New":
    #         # print(a_result[i].rstrip("New"))
    #         a_result = a_result[i].rstrip("New")
    #         return a_result,
    #     else:
    #         # print(a_result[i])
    #         return a_box[i]
    #     # print(url_result[i])
    #     return url_box[i]

    # return a_result,url_result
# ans = get_news()
# print(ans)
# result = []
# for i in range(len(result1)):
#     result.append(result1[i]+"\n"+"https://www.nishinippon.co.jp/"+result2[i]+"\n\n")
# print('\n'.join(result))
# print(result)
# get_news()