import requests
from bs4 import BeautifulSoup

def get_yahoo_news_urls():
    """
    야후 파이낸스 '최신 뉴스' 페이지에서 기사 URL 목록을 추출합니다.
    """
    # 크롤링할 목표 URL
    url = "https://finance.yahoo.com/topic/stock-market-news/"
    
    # 봇 차단을 피하기 위해 웹 브라우저처럼 보이게 하는 헤더 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    } 

    # 설정한 URL과 헤더로 웹 페이지에 요청을 보냄
    response = requests.get(url, headers=headers) 
    print(f"Status Code: {response.status_code}")  # 접속 상태 확인 (200이면 성공) [cite: 578]

    # HTML을 파싱하기 위한 BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, 'html.parser') 
    
    # 추출된 URL을 저장할 빈 리스트 생성
    results = [] 
    
    # 뉴스 기사들이 포함된 <li> 태그들을 모두 선택
    # PDF에서 li:nth-child() 패턴을 통해 확인된 리스트 구조를 타겟팅합니다. [cite: 508, 509, 617, 618]
    items = soup.find_all('li', class_='stream-item')

    # 가져온 목록을 순회하며 링크 추출
    for item in items:
        # 'ad-item' 클래스가 포함된 항목(광고)은 건너뜀 [cite: 570, 584, 591]
        if 'ad-item' in item.get('class', []):
            continue
        
        # <li> 태그 내에서 href 속성이 있는 <a> 태그를 찾음 [cite: 426, 588, 623]
        link_tag = item.find('a', href=True)
        
        # <a> 태그가 존재하면 href 속성(URL)을 results 리스트에 추가
        if link_tag:
            results.append(link_tag['href']) 
            
    return results

# 함수 실행 및 결과 확인
if __name__ == "__main__":
    news_urls = get_yahoo_news_urls()
    print("\n---추출된 뉴스 URL---")
    for url in news_urls:
        print(url)