# translate.py
# (프로그램 레벨 주석: 이 스크립트는 Hugging Face의 MarianMT 모델을 사용해 
#  일본어 텍스트를 영어로 번역하는 기능을 담당합니다.)

# 1. 필요한 라이브러리 임포트
from transformers import MarianMTModel, MarianTokenizer

# (블록 레벨 주석: 모델 이름 정의 및 모델/토크나이저 로드)
# 'Helsinki-NLP/opus-mt-ja-en'는 일본어(ja) -> 영어(en) 번역을 위해
# 사전 훈련된(pre-trained) 모델입니다.
try:
    print("Loading model and tokenizer...")
    MODEL_NAME = "Helsinki-NLP/opus-mt-ja-en"
    tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
    model = MarianMTModel.from_pretrained(MODEL_NAME)
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    # (모델 로드 실패 시 종료)
    exit()

def translate_japanese_to_english(text_to_translate):
    """
    입력된 일본어 텍스트를 영어로 번역합니다.

    Args:
        text_to_translate (str): 번역할 일본어 문장

    Returns:
        str: 영어로 번역된 문장
    """
    
    # (블록 레벨 주석: 번역 파이프라인)
    # 1. 텍스트를 모델이 이해할 수 있는 숫자(토큰)로 변환 (토크나이징)
    #    return_tensors="pt"는 PyTorch 텐서(데이터 묶음)로 반환하라는 의미입니다.
    tokenized_text = tokenizer(text_to_translate, return_tensors="pt", padding=True)
    
    # 2. 모델을 사용해 번역된 토큰 생성 (추론)
    translated_tokens = model.generate(**tokenized_text)
    
    # 3. 번역된 숫자(토큰)를 다시 사람이 읽을 수 있는 텍스트로 변환 (디코딩)
    translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    
    return translation

# --- 이 스크립트를 직접 실행했을 때만 테스트 코드가 동작하도록 함 ---
if __name__ == "__main__":
    # (블록 레벨 주석: 테스트용 예시 문장)
    test_sentence_1 = "私は学生です。"
    test_sentence_2 = "今日はいい天気ですね。"
    
    print("--- Translation Test Start ---")
    
    # 테스트 1
    translated_1 = translate_japanese_to_english(test_sentence_1)
    print(f"Original (ja): {test_sentence_1}")
    print(f"Translated (en): {translated_1}")
    print("-" * 20)
    
    # 테스트 2
    translated_2 = translate_japanese_to_english(test_sentence_2)
    print(f"Original (ja): {test_sentence_2}")
    print(f"Translated (en): {translated_2}")
    
    print("--- Translation Test End ---")