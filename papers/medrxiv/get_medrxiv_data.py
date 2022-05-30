import sys
import os
import requests
from bs4 import BeautifulSoup


def medrxiv_data(keyword: str) -> list:
    url = f"https://www.medrxiv.org/search/{keyword}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    titles = soup.select("div > span > a")

    data_list = []
    for title in titles:
        dic = {"link": "https://www.medrxiv.org" + title.get("href")}
        dic["title"] = title.span.text
        dic["time"] = str(title.get("href")).split(
            "/")[-1][:10].replace('.', "")
        data_list.append(dic)

        # 下载
        file_name = f'{dic["title"]}.pdf'
        if (file_name not in os.listdir("./paper_pdf")) & (int(dic["time"]) > 20200101):
            pdf_url = dic["link"] + ".full.pdf"
            r = requests.get(pdf_url)
            with open(f"./paper_pdf/{file_name}", 'wb') as f:
                f.write(r.content)

    return data_list


def get_list(key_list: list) -> list:
    data_list = []
    for i in key_list:
        once_data = medrxiv_data(i)
        data_list.extend(once_data)
    data_list = [dict(t) for t in {tuple(d.items()) for d in data_list}]
    return data_list


# data = get_list(["2019-nCoV", "Novel coronavirus"])
# print(data)

# print(os.listdir("../paper_pdf"))
