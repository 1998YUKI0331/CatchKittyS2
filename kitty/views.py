from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Input, InputTemp
from .forms import InputForm, InputTempForm
import requests
from bs4 import BeautifulSoup
import json
import time
# Create your views here.

def home(request):
    returns = { "r_keyword": "-0",
                "r_max_price": 0, }
    if request.method == 'POST':
        form = InputTempForm(request.POST)
        if form.is_valid():
            input = form.save(commit=False)
            returns["r_keyword"] = input.keyword
            returns["r_max_price"] = input.max_price
            return search(request, input.keyword, input.max_price)
    else:
        form = InputTempForm()
    context = {'form': form}
    return render(request, 'home.html', context)

def create(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            input = form.save(commit=False)
            input.save()
            return redirect('kitty:home')
    else:
        form = InputForm()
    context = {'form': form}
    return render(request, 'create.html', context)


def search(request, keyword, max_price):
    returns = { "r_title": "-0",
                "r_image": "-0",
                "r_price": "-0",
                "r_link": "-0", }
    
    url = "https://saladmarket.co.kr/product/search.html?banner_action=&keyword={}".format(keyword)
    r = requests.get(url, headers = {"User-Agent" : "Mozilla/5.0"}) #403 error 때문에 headers 추가
    bs = BeautifulSoup(r.content, "lxml") #lxml이란 파서로 분석
    divs = bs.select("div.description") #select 결과는 list
    dimg = bs.select("div.prdImg")

    for d in dimg: #이거 안쓰고 divs에서 쓸거야
        images = d.select("img")[0]
        image = (images.get("src")) #제품 이미지
        title = (images.get("alt")) #제품 타이틀
        title = title[:-5] #이름 뒤에 샐러드마켓 붙는거 빼

        print(title)
        print(image)

    for d in divs:
        p_list = d.find_all(style="font-size:14px;color:#555555;font-weight:bold;") #가격 인덱스로 접근해서 찾으려고
        n_list = d.find_all(style="font-size:14px;color:#555555;")
        links = d.select("a")[0]
        link = (links.get("href"))
        link = "https://saladmarket.co.kr" + link #제품 링크

        name_text = ''
        name_text = name_text.join(n_list[1])

        price_text = ''
        price_text = price_text.join(p_list[1])[1:][:-1] #제품 가격
        price_text = price_text.replace(",","")
        price_int = int(price_text)

        if price_int <= max_price:
            #text = "{} ₩{}원\n{}".format(title, price_text, link)
            returns["r_title"] = title
            returns["r_image"] = image
            returns["r_price"] = price_text
            returns["r_link"] = link


    return render(request, 'search.html', returns)