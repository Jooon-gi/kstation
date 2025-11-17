#!/usr/bin/env python3
"""
complete-shopify 폴더의 모든 HTML 파일에 FAQ/아코디언 기본 펼침 상태 적용 스크립트
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict

def find_html_files(root_dir: str) -> List[str]:
    """모든 HTML 파일 찾기"""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in root:
            continue
        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(os.path.join(root, file))
    return html_files

def fix_details_tags(content: str) -> Tuple[str, int]:
    """<details> 태그에 open 속성 추가"""
    count = 0
    
    def add_open(match):
        nonlocal count
        tag = match.group(0)
        if 'open' not in tag.lower():
            if tag.endswith('>'):
                new_tag = tag[:-1] + ' open>'
            else:
                new_tag = tag.replace('>', ' open>', 1)
            count += 1
            return new_tag
        return tag
    
    pattern = r'<details\s+[^>]*>|<details>'
    content = re.sub(pattern, add_open, content, flags=re.IGNORECASE)
    
    return content, count

def fix_aria_expanded(content: str) -> Tuple[str, int]:
    """aria-expanded="false"를 "true"로 변경"""
    count = 0
    
    def replace_false(match):
        nonlocal count
        count += 1
        return match.group(0).replace('false', 'true', 1)
    
    pattern = r'aria-expanded\s*=\s*["\']false["\']'
    content = re.sub(pattern, replace_false, content, flags=re.IGNORECASE)
    
    return content, count

def fix_ac_panel_show(content: str) -> Tuple[str, int]:
    """ac-panel에 show 클래스 추가"""
    count = 0
    
    def add_show(match):
        nonlocal count
        tag = match.group(0)
        if 'kst-show' not in tag.lower() and 'show' not in tag.lower():
            if 'class=' in tag:
                tag = re.sub(
                    r'class\s*=\s*["\']([^"\']*)["\']',
                    lambda m: f'class="{m.group(1)} kst-show"',
                    tag,
                    flags=re.IGNORECASE
                )
            else:
                tag = tag.replace('>', ' class="kst-show">', 1)
            count += 1
        return tag
    
    pattern = r'<div\s+[^>]*class\s*=\s*["\'][^"\']*ac-panel[^"\']*["\'][^>]*>'
    content = re.sub(pattern, add_show, content, flags=re.IGNORECASE)
    
    return content, count

def fix_faq_answer_active(content: str) -> Tuple[str, int]:
    """kst-faq-answer에 kst-active 클래스 추가 (answer가 아닌 경우만)"""
    count = 0
    
    def add_active(match):
        nonlocal count
        tag = match.group(0)
        # answer가 아닌 경우만 처리
        if 'answer' not in tag.lower() and 'kst-active' not in tag.lower() and 'active' not in tag.lower():
            if 'class=' in tag:
                tag = re.sub(
                    r'class\s*=\s*["\']([^"\']*)["\']',
                    lambda m: f'class="{m.group(1)} kst-active"',
                    tag,
                    flags=re.IGNORECASE
                )
            else:
                tag = tag.replace('>', ' class="kst-active">', 1)
            count += 1
        return tag
    
    # .kst-faq 또는 .faq 클래스를 가진 div 찾기 (answer 제외)
    pattern = r'<div\s+[^>]*class\s*=\s*["\'][^"\']*faq[^"\']*["\'][^>]*>'
    content = re.sub(pattern, add_active, content, flags=re.IGNORECASE)
    
    # .kst-faq-answer에 kst-active 추가
    def add_active_to_answer(match):
        nonlocal count
        tag = match.group(0)
        if 'kst-active' not in tag.lower():
            if 'class=' in tag:
                tag = re.sub(
                    r'class\s*=\s*["\']([^"\']*)["\']',
                    lambda m: f'class="{m.group(1)} kst-active"',
                    tag,
                    flags=re.IGNORECASE
                )
            else:
                tag = tag.replace('>', ' class="kst-active">', 1)
            count += 1
        return tag
    
    answer_pattern = r'<div\s+[^>]*class\s*=\s*["\'][^"\']*faq-answer[^"\']*["\'][^>]*>'
    content = re.sub(answer_pattern, add_active_to_answer, content, flags=re.IGNORECASE)
    
    # 잘못 추가된 answer의 active 제거 (중복 방지)
    content = re.sub(
        r'class\s*=\s*["\']([^"\']*faq-answer[^"\']*)\s+kst-active\s+kst-active["\']',
        r'class="\1 kst-active"',
        content,
        flags=re.IGNORECASE
    )
    
    return content, count

def fix_faq_item_open(content: str) -> Tuple[str, int]:
    """kst-faq-item에 kst-open 클래스 추가 (kst-open 패턴 사용하는 경우)"""
    count = 0
    
    def add_open(match):
        nonlocal count
        tag = match.group(0)
        if 'kst-open' not in tag.lower():
            if 'class=' in tag:
                tag = re.sub(
                    r'class\s*=\s*["\']([^"\']*)["\']',
                    lambda m: f'class="{m.group(1)} kst-open"',
                    tag,
                    flags=re.IGNORECASE
                )
            else:
                tag = tag.replace('>', ' class="kst-open">', 1)
            count += 1
        return tag
    
    # .kst-faq-item에 kst-open 추가 (이미 kst-active가 있는 경우만)
    pattern = r'<div\s+[^>]*class\s*=\s*["\'][^"\']*faq-item[^"\']*kst-active[^"\']*["\'][^>]*>'
    content = re.sub(pattern, add_open, content, flags=re.IGNORECASE)
    
    return content, count

def process_file(file_path: str) -> dict:
    """단일 파일 처리"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 수정 적용
        stats = {
            'details': 0,
            'aria_expanded': 0,
            'ac_panel': 0,
            'faq_answer': 0,
            'faq_item_open': 0
        }
        
        content, stats['details'] = fix_details_tags(content)
        content, stats['aria_expanded'] = fix_aria_expanded(content)
        content, stats['ac_panel'] = fix_ac_panel_show(content)
        content, stats['faq_answer'] = fix_faq_answer_active(content)
        content, stats['faq_item_open'] = fix_faq_item_open(content)
        
        # 변경사항이 있으면 저장
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {
                'modified': True,
                'stats': stats
            }
        else:
            return {
                'modified': False,
                'stats': stats
            }
    
    except Exception as e:
        return {'modified': False, 'error': str(e)}

def main():
    """메인 함수"""
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'complete-shopify')
    
    if not os.path.exists(root_dir):
        print(f"❌ 디렉토리를 찾을 수 없습니다: {root_dir}")
        return
    
    html_files = find_html_files(root_dir)
    
    print(f"📁 총 {len(html_files)}개의 HTML 파일을 찾았습니다.\n")
    print("=" * 70)
    print("complete-shopify 폴더 FAQ/아코디언 패턴 수정 중...")
    print("=" * 70)
    
    total_stats = {
        'details': 0,
        'aria_expanded': 0,
        'ac_panel': 0,
        'faq_answer': 0,
        'faq_item_open': 0
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
            if stats['aria_expanded'] > 0:
                changes.append(f"aria-expanded: {stats['aria_expanded']}")
            if stats['ac_panel'] > 0:
                changes.append(f"ac-panel: {stats['ac_panel']}")
            if stats['faq_answer'] > 0:
                changes.append(f"faq-answer: {stats['faq_answer']}")
            if stats['faq_item_open'] > 0:
                changes.append(f"faq-item-open: {stats['faq_item_open']}")
            
            if changes:
                print(f"✅ {os.path.basename(file_path)} - {', '.join(changes)}")
    
    print("\n" + "=" * 70)
    print("📊 수정 완료 요약")
    print("=" * 70)
    print(f"총 파일 수: {len(html_files)}")
    print(f"수정된 파일: {len(modified_files)}")
    print(f"오류 발생: {len(error_files)}")
    print(f"\n총 변경 사항:")
    print(f"  - <details> 태그: {total_stats['details']}개")
    print(f"  - aria-expanded: {total_stats['aria_expanded']}개")
    print(f"  - ac-panel: {total_stats['ac_panel']}개")
    print(f"  - faq-answer: {total_stats['faq_answer']}개")
    print(f"  - faq-item-open: {total_stats['faq_item_open']}개")
    
    if error_files:
        print(f"\n⚠️ 오류 발생 파일:")
        for file_path, error in error_files:
            print(f"  - {os.path.basename(file_path)}: {error}")

if __name__ == '__main__':
    main()

