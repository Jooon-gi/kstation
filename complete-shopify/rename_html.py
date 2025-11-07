import os
import re

# --- 설정 ---
FOLDER_PATH = '.'
SEPARATOR = '-'
EXTENSIONS = ('.html', '.htm') 
# ------------------------------

def rename_files_for_dev(folder_path, separator, extensions):
    """
    지정된 폴더 내의 파일을 개발 친화적인 이름으로 일괄 변경합니다.
    - 소문자 변환
    - 공백을 지정된 구분 기호로 대체 (하이픈 '-')
    - 허용되지 않는 특수 문자 제거
    - 연속된 구분 기호(하이픈)를 단일 구분 기호로 압축 (새로 추가된 기능)
    """
    
    print(f"--- 파일명 일괄 변경을 시작합니다 (대상 폴더: {folder_path}) ---")
    
    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(extensions):
                
                old_full_path = os.path.join(folder_path, filename)
                
                # 파일명과 확장자 분리
                base_name, ext = os.path.splitext(filename)
                
                # 1. 소문자로 변환
                new_base_name = base_name.lower()
                
                # 2. 공백을 구분 기호로 대체
                new_base_name = new_base_name.replace(' ', separator)
                
                # 3. 허용되지 않는 특수 문자 제거
                # a-z, 0-9, 설정된 구분자(-)를 제외한 모든 문자 제거
                new_base_name = re.sub(f'[^{re.escape(separator)}a-z0-9]', '', new_base_name)
                
                # 4. 🔥 연속된 구분자(하이픈)를 단일 구분자로 압축 (새로 추가된 부분)
                # '----' 와 같은 연속된 문자를 '-' 하나로 바꿉니다.
                new_base_name = re.sub(f'{re.escape(separator)}{{2,}}', separator, new_base_name)
                
                # 5. 파일명이 하이픈으로 시작하거나 끝나는 경우 제거 (선택 사항이지만 깔끔하게 만듦)
                new_base_name = new_base_name.strip(separator)

                # 최종 파일명 재조합
                new_filename = new_base_name + ext.lower()

                # 파일명이 실제로 변경되는지 확인
                if filename != new_filename:
                    new_full_path = os.path.join(folder_path, new_filename)
                    # 파일명 변경 실행
                    os.rename(old_full_path, new_full_path)
                    print(f"[변경 완료] {filename} -> {new_filename}")
                else:
                    print(f"[변경 없음] {filename} (이미 개발 친화적인 이름입니다)")

    except Exception as e:
        print(f"\n[오류 발생] 파일 변경 중 문제가 발생했습니다: {e}")

if __name__ == "__main__":
    rename_files_for_dev(FOLDER_PATH, SEPARATOR, EXTENSIONS)
    print("\n--- 모든 HTML 파일명 변경 완료 ---")