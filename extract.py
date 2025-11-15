# extract.py (수정된 버전)
# (프로그램 레벨 주석: GiNZA(spaCy) 모델을 사용해 일본어 텍스트에서
#  의미 있는 한자 단어(명사, 동사 등)의 원형을 추출합니다.)

import spacy
import re # (한자 정규식 확인을 위해 re 라이브러리 임포트)

# (블록 레벨 주석: 1. GiNZA AI 모델 로드)
# "ja_ginza"는 'pip install ginza'로 설치된 모델 이름입니다.
MODEL_NAME = "ja_ginza"
try:
    print(f"Loading GiNZA model ({MODEL_NAME})...")
    nlp = spacy.load(MODEL_NAME)
    print("Model loaded successfully.")
except OSError:
    # (OSError는 모델을 찾지 못할 때 발생합니다)
    print(f"Error: Could not find model '{MODEL_NAME}'.")
    print("Please make sure 'ginza' is installed correctly via 'pip install ginza'")
    exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()


# (블록 레벨 주석: 2. 한자(Kanji)를 찾는 정규식)
# CJK Unified Ideographs (중국/일본/한국 한자 범위)
KANJI_REGEX = re.compile(r'[\u4e00-\u9faf]')

def extract_kanji_words(text_to_extract):
    """
    GiNZA 모델을 사용해 텍스트에서 한자가 포함된 의미 있는 단어(명사, 동사, 형용사 등)의
    '사전 원형(lemma)'을 추출합니다.

    Args:
        text_to_extract (str): 분석할 일본어 문장

    Returns:
        list: 한자 단어(원형)의 리스트 (중복 제거됨)
    """
    
    # (블록 레벨 주석: 3. AI 모델로 텍스트 분석)
    doc = nlp(text_to_extract)
    
    # 중복을 자동으로 제거하기 위해 set() 자료형 사용
    kanji_words_set = set()
    
    # (블록 레벨 주석: 4. 분석된 토큰(token)들을 순회)
    for token in doc:
        # 4-1. Anki 카드에 올릴 만한 품사인지 확인 (명사, 고유명사, 동사, 형용사)
        is_meaningful_pos = token.pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ']
        
        # 4-2. 해당 단어의 텍스트에 한자가 1개라도 포함되어 있는지 확인
        has_kanji = bool(KANJI_REGEX.search(token.text))

        if is_meaningful_pos and has_kanji:
            # (블록 레벨 주석: 5. '사전 원형(lemma_)'을 리스트에 추가)
            kanji_words_set.add(token.lemma_)
            
    # set을 list로 변환하여 반환
    return list(kanji_words_set)

# --- 이 스크립트를 직접 실행했을 때만 테스트 코드가 동작하도록 함 ---
if __name__ == "__main__":
    test_sentence = "明日会社でお会いしましょう。"
    
    print("--- Kanji Extraction Test Start ---")
    print(f"Original: {test_sentence}")
    
    extracted_words = extract_kanji_words(test_sentence)
    
    print(f"Extracted Kanji Words (Lemmas): {extracted_words}")
    print("--- Kanji Extraction Test End ---")