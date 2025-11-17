#!/usr/bin/env python3
"""
HTML 파일들의 아코디언/FAQ 컴포넌트를 기본적으로 "펼쳐진 상태"로 만드는 스크립트

패턴 분석 결과:
1. <details><summary> 태그 - open 속성 추가 필요
2. .kst-ac-item + aria-expanded + .kst-show - aria-expanded="true" 및 .kst-show 클래스 추가
3. .kst-faq + .kst-active - .kst-active 클래스 추가
4. .kst-faq-item (단순 표시) - 변경 불필요
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

def find_html_files(root_dir: str) -> List[str]:
    """모든 HTML 파일 찾기"""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # .git 디렉토리 제외
        if '.git' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def fix_details_tags(content: str) -> Tuple[str, int]:
    """<details> 태그에 open 속성 추가"""
    count = 0
    
    # <details> 태그에 open 속성이 없으면 추가
    # 단, 이미 open이 있거나 특정 클래스 내부가 아닌 경우만 처리
    def add_open(match):
        nonlocal count
        tag = match.group(0)
        if 'open' not in tag.lower():
            # open 속성 추가
            if tag.endswith('>'):
                new_tag = tag[:-1] + ' open>'
            else:
                new_tag = tag.replace('>', ' open>', 1)
            count += 1
            return new_tag
        return tag
    
    # <details> 태그 찾기 및 수정
    pattern = r'<details\s+[^>]*>|<details>'
    content = re.sub(pattern, add_open, content, flags=re.IGNORECASE)
    
    return content, count

def fix_kst_ac_items(content: str) -> Tuple[str, int]:
    """kst-ac-item 패턴 수정: aria-expanded="false" -> "true", .kst-show 클래스 추가"""
    count = 0
    
    # kst-ac-item 블록 전체를 찾아서 처리
    # 각 .kst-ac-item 블록을 찾아서 aria-expanded와 panel을 함께 수정
    def process_ac_item_block(match):
        nonlocal count
        block = match.group(0)
        original_block = block
        
        # aria-expanded="false"를 "true"로 변경
        block = re.sub(
            r'aria-expanded="false"',
            'aria-expanded="true"',
            block,
            flags=re.IGNORECASE
        )
        
        # .kst-ac-panel에 .kst-show 클래스 추가
        def add_show_to_panel(panel_match):
            panel_tag = panel_match.group(0)
            if 'kst-show' not in panel_tag:
                if 'class=' in panel_tag:
                    panel_tag = re.sub(
                        r'class="([^"]*)"',
                        r'class="\1 kst-show"',
                        panel_tag,
                        flags=re.IGNORECASE
                    )
                else:
                    if 'id=' in panel_tag:
                        panel_tag = re.sub(
                            r'(id="[^"]*")',
                            r'\1 class="kst-show"',
                            panel_tag,
                            flags=re.IGNORECASE
                        )
                    else:
                        panel_tag = panel_tag.replace('>', ' class="kst-show">', 1)
            return panel_tag
        
        block = re.sub(
            r'<div\s+[^>]*class="[^"]*kst-ac-panel[^"]*"[^>]*>',
            add_show_to_panel,
            block,
            flags=re.IGNORECASE
        )
        
        # 버튼의 span 텍스트도 변경 (+ -> -)
        block = re.sub(
            r'(<span>)\s*[＋+]\s*(</span>)',
            r'\1−\2',
            block
        )
        
        if block != original_block:
            count += 1
        
        return block
    
    # .kst-ac-item 블록을 찾아서 처리 (다음 .kst-ac-item 또는 닫는 태그까지)
    # 간단한 방법: 각 패턴을 개별적으로 수정
    content = re.sub(
        r'aria-expanded="false"',
        'aria-expanded="true"',
        content,
        flags=re.IGNORECASE
    )
    
    # .kst-ac-panel에 .kst-show 추가
    def add_show_class(match):
        nonlocal count
        panel_tag = match.group(0)
        if 'kst-show' not in panel_tag:
            if 'class=' in panel_tag:
                panel_tag = re.sub(
                    r'class="([^"]*)"',
                    r'class="\1 kst-show"',
                    panel_tag,
                    flags=re.IGNORECASE
                )
            else:
                if 'id=' in panel_tag:
                    panel_tag = re.sub(
                        r'(id="[^"]*")',
                        r'\1 class="kst-show"',
                        panel_tag,
                        flags=re.IGNORECASE
                    )
                else:
                    panel_tag = panel_tag.replace('>', ' class="kst-show">', 1)
            count += 1
        return panel_tag
    
    content = re.sub(
        r'<div\s+[^>]*class="[^"]*kst-ac-panel[^"]*"[^>]*>',
        add_show_class,
        content,
        flags=re.IGNORECASE
    )
    
    # 버튼의 span 텍스트 변경 (+ -> -)
    # aria-expanded="true"인 항목의 span만 변경
    def update_span_text(match):
        span_content = match.group(0)
        # ＋ 또는 +를 −로 변경
        if '＋' in span_content or '+' in span_content:
            span_content = re.sub(r'[＋+]', '−', span_content)
        return span_content
    
    # aria-expanded="true"인 .kst-ac-item 내부의 span만 찾아서 변경
    # 간단하게: 모든 ＋ 또는 +를 −로 변경 (aria-expanded="true" 근처의 것만)
    # 더 정확하게는 블록 단위로 처리해야 하지만, 일단 간단하게 처리
    content = re.sub(
        r'(<div\s+[^>]*aria-expanded="true"[^>]*>.*?<span>)\s*[＋+]\s*(</span>)',
        r'\1−\2',
        content,
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # aria-expanded 변경 횟수 계산
    aria_count = len(re.findall(r'aria-expanded="true"', content, re.IGNORECASE))
    
    return content, max(count, aria_count)

def fix_kst_faq_items(content: str) -> Tuple[str, int]:
    """kst-faq 패턴 수정: .kst-active 클래스 추가"""
    count = 0
    
    # .kst-faq에 .kst-active 클래스 추가 (없는 경우만)
    def add_active_class(match):
        nonlocal count
        faq_tag = match.group(0)
        if 'kst-active' not in faq_tag:
            # class 속성이 있으면 추가
            if 'class=' in faq_tag:
                faq_tag = re.sub(
                    r'class="([^"]*)"',
                    r'class="\1 kst-active"',
                    faq_tag,
                    flags=re.IGNORECASE
                )
            else:
                faq_tag = faq_tag.replace('>', ' class="kst-active">', 1)
            count += 1
        return faq_tag
    
    content = re.sub(
        r'<div\s+[^>]*class="[^"]*kst-faq[^"]*"[^>]*>',
        add_active_class,
        content,
        flags=re.IGNORECASE
    )
    
    return content, count

def fix_kst_faq_question_pattern(content: str) -> Tuple[str, int]:
    """kst-faq-question 패턴 수정 (a06 등): 부모 .kst-faq에 .kst-active 추가"""
    count = 0
    
    # .kst-faq div에 .kst-active 클래스 추가 (없는 경우만)
    # 단, .kst-faq-answer에는 추가하지 않음
    def add_active_to_faq(match):
        nonlocal count
        faq_tag = match.group(0)
        # .kst-faq-answer가 아닌 경우만 처리
        if 'kst-faq-answer' not in faq_tag and 'kst-active' not in faq_tag:
            # class 속성에 kst-active 추가
            faq_tag = re.sub(
                r'class="([^"]*)"',
                r'class="\1 kst-active"',
                faq_tag,
                flags=re.IGNORECASE
            )
            count += 1
        return faq_tag
    
    # <div class="kst-faq" 패턴 찾기 (kst-faq-answer 제외)
    content = re.sub(
        r'<div\s+class="[^"]*kst-faq[^"]*"[^>]*>',
        add_active_to_faq,
        content,
        flags=re.IGNORECASE
    )
    
    # 잘못 추가된 .kst-faq-answer의 kst-active 제거
    content = re.sub(
        r'class="([^"]*kst-faq-answer[^"]*)\s+kst-active"',
        r'class="\1"',
        content,
        flags=re.IGNORECASE
    )
    
    return content, count

def process_file(file_path: str) -> dict:
    """단일 파일 처리"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        stats = {
            'details': 0,
            'ac_items': 0,
            'faq_items': 0,
            'faq_question': 0
        }
        
        # 패턴별 수정
        content, stats['details'] = fix_details_tags(content)
        content, stats['ac_items'] = fix_kst_ac_items(content)
        content, stats['faq_items'] = fix_kst_faq_items(content)
        content, stats['faq_question'] = fix_kst_faq_question_pattern(content)
        
        # 변경사항이 있으면 파일 저장
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {'modified': True, 'stats': stats}
        else:
            return {'modified': False, 'stats': stats}
    
    except Exception as e:
        return {'modified': False, 'error': str(e)}

def main():
    """메인 함수"""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    html_files = find_html_files(root_dir)
    
    print(f"📁 총 {len(html_files)}개의 HTML 파일을 찾았습니다.\n")
    print("=" * 60)
    print("아코디언/FAQ 컴포넌트 기본 상태를 '펼쳐짐'으로 변경 중...")
    print("=" * 60)
    
    total_stats = {
        'details': 0,
        'ac_items': 0,
        'faq_items': 0,
        'faq_question': 0
    }
    modified_files = []
    error_files = []
    
    for file_path in html_files:
        result = process_file(file_path)
        
        if 'error' in result:
            error_files.append((file_path, result['error']))
            print(f"❌ 오류: {os.path.basename(file_path)} - {result['error']}")
        elif result['modified']:
            modified_files.append(file_path)
            stats = result['stats']
            for key in total_stats:
                total_stats[key] += stats[key]
            
            changes = []
            if stats['details'] > 0:
                changes.append(f"details: {stats['details']}")
            if stats['ac_items'] > 0:
                changes.append(f"ac-items: {stats['ac_items']}")
            if stats['faq_items'] > 0:
                changes.append(f"faq-items: {stats['faq_items']}")
            if stats['faq_question'] > 0:
                changes.append(f"faq-question: {stats['faq_question']}")
            
            if changes:
                print(f"✅ {os.path.basename(file_path)} - {', '.join(changes)}")
    
    print("\n" + "=" * 60)
    print("📊 수정 완료 요약")
    print("=" * 60)
    print(f"총 파일 수: {len(html_files)}")
    print(f"수정된 파일: {len(modified_files)}")
    print(f"오류 발생: {len(error_files)}")
    print(f"\n총 변경 사항:")
    print(f"  - <details> 태그: {total_stats['details']}개")
    print(f"  - .kst-ac-item: {total_stats['ac_items']}개")
    print(f"  - .kst-faq: {total_stats['faq_items']}개")
    print(f"  - .kst-faq-question: {total_stats['faq_question']}개")
    
    if error_files:
        print(f"\n⚠️ 오류 발생 파일:")
        for file_path, error in error_files:
            print(f"  - {os.path.basename(file_path)}: {error}")

if __name__ == '__main__':
    main()

