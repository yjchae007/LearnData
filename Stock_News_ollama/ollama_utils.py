import ollama

# --- Ollama 모델 설정 ---
OLLAMA_MODEL = 'gemma3n:e2b'

def process_with_ollama(text, task):
    """
    로컬 Ollama의 지정된 모델을 사용하여 요약 또는 번역 작업을 수행합니다.
    :param text: 처리할 텍스트
    :param task: 'summarize' 또는 'translate'
        - 'summarize': 본문(body) 요약에 사용
        - 'translate': 제목(title) 번역, 본문 번역, 요약문 번역에 사용
    :return: 처리된 텍스트
    """
    try:
        if task == 'summarize':
            prompt = f"""You are a helpful assistant. Summarize the following news text into a 3 concise sentences. 
            Output only the summarized sentences. Focus on impact and significance.
            Text: '{text}' 
            Summary:"""
        elif task == 'translate':
            prompt = f"""You are an expert translator. Translate the following English text to Korean. 
            Output only the Korean translation.
            English: '{text}'
            Korean:"""
        else:
            return text

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        return response['message']['content'].strip()
    except Exception as e:
        print(f"Ollama 처리 중 오류 발생: {e}")
        print(f"Ollama가 실행 중인지, 모델({OLLAMA_MODEL})이 정상적으로 설치되었는지 확인하세요.")
        return f"Ollama 오류: 원문 반환" 