import requests
import pandas as pd
from bs4 import BeautifulSoup
from ollama_utils import process_with_ollama  # ollama 관련 함수 import
from datetime import datetime


def get_yahoo_stock_news():
    """
    Yahoo Stock '최신 뉴스' 페이지에서 기사 URL 목록을 추출합니다.
    """
    # 크롤링할 목표 URL
    url = "https://finance.yahoo.com/topic/stock-market-news/"
    
    # 봇 차단을 피하기 위해 웹 브라우저처럼 보이게 하는 헤더 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    } 

    # 설정한 URL과 헤더로 웹 페이지에 요청을 보냄
    response = requests.get(url, headers=headers) 
    print(f"Status Code: {response.status_code}")

    # HTML을 파싱하기 위한 BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, 'html.parser') 
    
    # 추출된 URL을 저장할 빈 리스트 생성
    results = [] 
    
    # 뉴스 기사들이 포함된 <li> 태그들을 모두 선택
    items = soup.find_all('li', class_='stream-item')

    # 가져온 목록을 순회하며 링크 추출
    for item in items:
        if 'ad-item' in item.get('class', []):
            continue
        link_tag = item.find('a', href=True)
        if link_tag:
            results.append(link_tag['href']) 
    return results


def main():
    print("Yahoo Stock 뉴스 크롤링을 시작합니다...")
    news_data = get_yahoo_stock_news()
    
    if not news_data:
        print("가져올 뉴스가 없습니다. 프로그램을 종료합니다.")
        return

    print(f"총 {len(news_data)}개의 뉴스를 발견했습니다. Ollama로 처리합니다...")
    
    processed_news = []
    crawled_date = datetime.now().strftime('%Y-%m-%d')
    
    # 로컬 모델 처리 시간 및 테스트를 위해 일부만 실행 (예: 5개)
    for i, news_url in enumerate(news_data[:]):
        print(f"({i+1}/{len(news_data[:])}) 처리 중: {news_url}")

        try:
            article_resp = requests.get(news_url, headers={ 'User-Agent': 'Mozilla/5.0' })
            article_soup = BeautifulSoup(article_resp.text, 'html.parser')
            # 제목 추출
            title_tag = article_soup.select_one('div.cover-headline')
            article_title = title_tag.get_text(strip=True) if title_tag else ''
            # 본문 추출
            body_tag = article_soup.select_one('div.body-wrap')
            article_body = body_tag.get_text(separator=' ', strip=True) if body_tag else ''
        except Exception as e:
            print(f"기사 제목/본문 추출 실패: {e}")
            article_title = news_url
            article_body = ''

        # 제목은 번역만
        title_ko = process_with_ollama(article_title, 'translate') if article_title else ''

        # 본문은 요약 및 번역
        body_summary_en = process_with_ollama(article_body, 'summarize') if article_body else ''
        body_summary_ko = process_with_ollama(body_summary_en, 'translate') if body_summary_en else ''

        processed_news.append({
            'Title': article_title,
            'Title (Korean)': title_ko,
            'Body Summary (English)': body_summary_en,
            'Body Summary (Korean)': body_summary_ko,
            'Link': news_url,
            'Crawled Date': crawled_date
        })

    if processed_news:
        df = pd.DataFrame(processed_news)
        output_filename = f'yahoo_stock_news_ollama_{crawled_date}.csv'
        df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        print(f"\n모든 작업이 완료되었습니다! '{output_filename}' 파일로 저장되었습니다.")
    else:
        print("\n처리된 뉴스가 없습니다.")

if __name__ == '__main__':
    main()