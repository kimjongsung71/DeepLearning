from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request
from urllib.error import HTTPError
import time
import os


# 검색어 입력
searchKey = input('검색할 키워드 입력 :')
getcnt    = input('저장 건수 입력 :')

# 폴더 생성
def createFolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except OSError:
        print('Error')

createFolder(f'train_dataset/{searchKey}')

################chome 실행###############################################################

driver = webdriver.Chrome()
driver.get('https://www.google.co.kr/imghp')

#################    쿼리 검색 및 검색 버튼 클릭 #########################################
elem = driver.find_element('name', 'q')
elem.send_keys(searchKey)
elem.send_keys(Keys.RETURN)

time.sleep(3)

#################  이미지 스크롤링 case 1 스크롤 끝까지 ####################################
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # 브라우저 끝까지 스크롤
    time.sleep(1) # 쉬어주기
    try:
        # button = driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input')
        button = driver.find_element(By.CLASS_NAME,'LZ4I')
        button.click() # 스크롤을 내리다보면 '결과 더보기'가 있는 경우 버튼 클릭
        time.sleep(1)
    except:
        pass
    if driver.find_element(By.CLASS_NAME, 'OuJzKb.Yu2Dnd').text == '더 이상 표시할 콘텐츠가 없습니다.': # class 이름으로 가져오기
        break

##############################################################################################

time.sleep(3)        
    
################ 이미지 수집 및 저장##########################################################

images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd") # 각 이미지들의 class
count = 1
for image in images:

    if count <= int(getcnt):
        try:
            image.click()
            time.sleep(1)
            imgUrl = driver.find_element(By.CSS_SELECTOR,".sFlh5c.pT0Scc.iPVvYb").get_attribute("src")
    # https로 요청할 경우 보안 문제로 SSL에러가 남    
            imgUrl = imgUrl.replace('https', 'http') 
    # 특정 사이트의 경우 봇이 접근하는 것을 차단해서  urllib.error.HTTPError: HTTP Error 403: Forbidden 발생
    # crawiling 방지 회피 : 아래와 같이 브라우저 인것 처럼 속이는 header를 추가
        #    opener = urllib.request.build_opener()
        #    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')] 
            # https://docs.python.org/3/library/urllib.request.html 참고
        #    urllib.request.install_opener(opener)  
        # 생성된 폴더에 해당 이미지 Down  
            urllib.request.urlretrieve(imgUrl, f'train_dataset/{searchKey}/{searchKey}_{str(count)}.jpg')
            
            count = count + 1

        except Exception as e:
    #        print('Error : ', e)
            pass
    else: 
    #     print("저장완료되었습니다")
        break 


driver.close()