# main.py
# (프로그램 레벨 주석: 이 스크립트는 프로젝트의 메인 파이프라인입니다.
#  translate.py와 extract.py의 기능을 가져와 사용자 입력을 처리하고,
#  Anki용 CSV 파일을 생성합니다.)

# (블록 레벨 주석: 1. 필요한 모듈 임포트)
import csv
import os
from translate import translate_japanese_to_english # 2단계에서 만든 번역 함수
from extract import extract_kanji_words   # 3단계에서 만든 한자 추출 함수

# (블록 레벨 주석: 2. 상수 정의)
# Anki가 인식할 CSV 파일 이름 정의
OUTPUT_CSV_FILE = "anki_deck.csv"
FIELDNAMES = ["Front", "Back"] # Anki 카드의 '앞면', '뒷면' 필드 이름

def initialize_csv():
    """CSV 파일이 존재하지 않으면, 헤더(Front, Back)를 추가합니다."""
    if not os.path.exists(OUTPUT_CSV_FILE):
        with open(OUTPUT_CSV_FILE, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
        print(f"Created new file: {OUTPUT_CSV_FILE}")

def add_to_csv(word, example_sentence, translation):
    """
    CSV 파일에 새로운 Anki 카드 데이터를 '누적' (append)합니다.
    """
    # (블록 레벨 주석: 3. Anki 카드 형식 생성)
    # 앞면: 한자 단어
    # 뒷면: 예문 (줄바꿈 <br>) 번역문
    front_text = word
    back_text = f"{example_sentence}<br>{translation}"
    
    # (블록 레벨 주석: 4. CSV 파일에 데이터 추가)
    # mode='a'는 'append' (누적) 모드를 의미합니다.
    with open(OUTPUT_CSV_FILE, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({"Front": front_text, "Back": back_text})

def main():
    """메인 실행 함수"""
    # 0. CSV 파일이 없으면 헤더를 생성합니다.
    initialize_csv()
    
    print("--- 🎌 Anki Kanji Card Builder 🎌 ---")
    print(f"Cards will be saved to: {OUTPUT_CSV_FILE}")
    print("Enter a Japanese sentence. (Type 'q' or 'exit' to quit)")
    
    # (블록 레벨 주석: 5. 사용자 입력을 받는 무한 루프)
    while True:
        try:
            # 1. 사용자로부터 일본어 문장 입력 받기
            sentence = input("\nSentence: ")
            
            # 2. 종료 명령어 확인
            if sentence.lower() in ['q', 'exit']:
                print("Exiting program. Goodbye!")
                break
                
            if not sentence:
                continue

            # (블록 레벨 주석: 6. AI 모델 파이프라인 실행)
            # 3. 2단계 모듈 호출 -> 번역 실행
            print("Translating...")
            translation = translate_japanese_to_english(sentence)
            
            # 4. 3단계 모듈 호출 -> 한자 단어 추출
            print("Extracting Kanji words...")
            kanji_words = extract_kanji_words(sentence)
            
            # 5. 결과 처리
            if not kanji_words:
                print("No meaningful Kanji words found in this sentence.")
                continue
                
            print(f"Found {len(kanji_words)} words: {', '.join(kanji_words)}")
            
            # 6. CSV에 저장
            for word in kanji_words:
                add_to_csv(word, sentence, translation)
            
            print(f"Successfully added {len(kanji_words)} card(s) to {OUTPUT_CSV_FILE}.")

        except KeyboardInterrupt:
            # (Ctrl+C로 종료 시)
            print("\nExiting program. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")

# --- 이 스크립트를 직접 실행했을 때만 main() 함수가 동작하도록 함 ---
if __name__ == "__main__":
    main()