import json
import time

KAKAO_TOKEN = "gCgmMM7TVph-BjAtGk56lQtePSeUlaR-ouJoNAorDNMAAAF5DZT-qg"
#https://developers.kakao.com/tool/rest-api/open/post/v2-api-talk-memo-default-send

send_lists = [] #보낸 데이타는 또 보내지 않으려고

def search_slickdeals(condition):
    keyword = condition["keyword"]
    min_price = condition["min_price"]
    max_price = condition["max_price"]

    url = "https://saladmarket.co.kr/product/search.html?banner_action=&keyword={}".format(keyword)
    r = requests.get(url, headers = {"User-Agent" : "Mozilla/5.0"}) #403 error 때문에 headers 추가
    bs = BeautifulSoup(r.content, "lxml") #lxml이란 파서로 분석
    divs = bs.select("div.description") #select 결과는 list
    dimg = bs.select("div.prdImg")

    for d in dimg: #이거 안쓰고 divs에서 쓸거야
        images = d.select("img")[0]
        image = (images.get("src")) #샐러드마켓에서 파는 헬로키티 제품 이미지
        title = (images.get("alt")) #샐러드마켓에서 파는 헬로키티 제품 타이틀
        title = title[:-5] #이름 뒤에 샐러드마켓 붙는거 빼

        #print(title)
        #print(image) 

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

        if min_price <= price_int <= max_price:
            send = True
            for s in send_lists:
                if s["title"] == title:
                    print("보낸적 있음~~")
                    send = False

        if send == True:
            text = "{}".format(title)
            r = send_to_kakao(text)
            print(r.text)
            send_lists.append({
                "title": title,
            })
            if send == True:
                text = "{} ₩{}원\n{}".format(title, price_text, link)
                r = send_to_kakao(text)
                print(r.text)
                send_lists.append({
                    "title": title,
                })

if __name__ == "__main__":
    condition = {
        "keyword": "헬로키티",
        "min_price": 10,
        "max_price": 30000
        #나중에 수정하든지...
    }
    
    while True:
        search_slickdeals(condition)
        time.sleep(60 * 5) #5분마다
