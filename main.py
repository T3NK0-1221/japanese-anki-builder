# main.py (OCR 통합 버전)

import csv
import os
import easyocr  # <-- 1. easyocr 임포트

# (블록 레벨 주석: 1. AI 모델들 전역 로드)
# 프로그램 시작 시 한 번만 로드하여 속도 향상
print("Loading AI models... (This may take a moment)")
try:
    # 2단계 모듈 (번역)
    from translate import translate_japanese_to_english
    
    # 3단계 모듈 (한자 추출)
    from extract import extract_kanji_words
    
    # OCR 모듈 (EasyOCR)
    # gpu=False (CPU 사용)
    OCR_READER = easyocr.Reader(['ja', 'en'], gpu=False) 
    print("All models loaded successfully.")

except ImportError as e:
    print(f"Error importing module: {e}")
    print("Please check your 'requirements.txt' and installations.")
    exit()
except Exception as e:
    print(f"Error loading models: {e}")
    exit()


# (블록 레벨 주석: 2. CSV 관련 함수들 - 수정 없음)
OUTPUT_CSV_FILE = "anki_deck.csv"
FIELDNAMES = ["Front", "Back"]

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
    (수정됨: 예문의 특정 단어를 <b> 태그로 감싸서 bold 처리합니다.)
    """
    front_text = word
    try:
        highlighted_sentence = example_sentence.replace(word, f"<b>{word}</b>")
    except:
        highlighted_sentence = example_sentence
    
    back_text = f"{highlighted_sentence}<br>{translation}"
    
    with open(OUTPUT_CSV_FILE, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({"Front": front_text, "Back": back_text})


# (블록 레벨 주석: 3. 핵심 파이프라인 함수)
# OCR 모드와 텍스트 모드에서 공통으로 사용할 함수
def process_sentence(sentence):
    """하나의 문장을 받아 번역, 한자 추출, CSV 저장을 수행합니다."""
    try:
        # 1. 번역 실행
        print(f"\nProcessing: {sentence}")
        print("Translating...")
        translation = translate_japanese_to_english(sentence)
        
        # 2. 한자 단어 추출
        print("Extracting Kanji words...")
        kanji_words = extract_kanji_words(sentence)
        
        # 3. 결과 처리
        if not kanji_words:
            print("No meaningful Kanji words found in this sentence.")
            return False
            
        print(f"Found {len(kanji_words)} words: {', '.join(kanji_words)}")
        
        # 4. CSV에 저장
        for word in kanji_words:
            add_to_csv(word, sentence, translation)
        
        print(f"Successfully added {len(kanji_words)} card(s) to {OUTPUT_CSV_FILE}.")
        return True
        
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        return False

# (블록 레벨 주석: 4. 모드 1 - 텍스트 입력)
def run_text_mode():
    """(기존 main 함수의 while 루프) 텍스트 입력을 받아 처리합니다."""
    print("\n--- 📝 Text Input Mode ---")
    print("Enter a Japanese sentence. (Type 'q' or 'exit' to quit)")
    
    while True:
        try:
            sentence = input("\nSentence: ")
            if sentence.lower() in ['q', 'exit']:
                break
            if not sentence:
                continue
                
            process_sentence(sentence) # 공통 함수 호출

        except KeyboardInterrupt:
            break

# (블록 레벨 주석: 5. 모드 2 - 이미지(OCR) 입력)
def run_ocr_mode():
    """이미지 경로를 입력받아 OCR로 텍스트를 추출하고 처리합니다."""
    print("\n--- 🖼️ Image (OCR) Mode ---")
    print("Enter the path to your image. (Type 'q' or 'exit' to quit)")

    while True:
        try:
            image_path = input("\nImage Path: ")
            if image_path.lower() in ['q', 'exit']:
                break
            
            # (따옴표 제거 - 드래그 앤 드롭 시)
            image_path = image_path.strip().strip('"') 

            if not os.path.exists(image_path):
                print("Error: File not found. Please check the path.")
                continue

            # (EasyOCR 실행)
            print("Running OCR on image... (This may take a moment)")
            # paragraph=True: 인식된 텍스트 조각들을 하나의 문단으로 합쳐줍니다.
            results = OCR_READER.readtext(image_path, paragraph=True) 

            if not results:
                print("No text detected in the image.")
                continue

            full_text = " ".join([res[1] for res in results])
            print(f"--- OCR Result --- \n{full_text}\n--------------------")

            # OCR 결과를 공통 처리 함수로 넘김
            process_sentence(full_text)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred in OCR mode: {e}")


# (블록 레벨 주석: 6. 메인 함수 - 라우터)
def main():
    """메인 실행 함수 (모드 선택)"""
    initialize_csv()
    
    print("--- 🎌 Anki Kanji Card Builder 🎌 ---")
    print(f"Cards will be saved to: {OUTPUT_CSV_FILE}")
    
    try:
        while True:
            print("\n" + "="*30)
            print("Select mode:")
            print("  [1] Type text manually")
            print("  [2] Use image (OCR)")
            print("  [q] Quit")
            mode = input("Choice (1, 2, or q): ").strip().lower()

            if mode == '1':
                run_text_mode()
            elif mode == '2':
                run_ocr_mode()
            elif mode == 'q':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or q.")
    except KeyboardInterrupt:
        print("\nExiting program. Goodbye!")


if __name__ == "__main__":
    main()