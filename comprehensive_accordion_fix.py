#!/usr/bin/env python3
"""
포괄적인 FAQ/아코디언 패턴 인식 및 수정 스크립트

이 스크립트는 특정 클래스명이나 접두사에 의존하지 않고,
실제 HTML 구조와 동작을 분석하여 FAQ/아코디언 패턴을 인식하고 수정합니다.
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

def detect_accordion_patterns(content: str) -> Dict[str, List]:
    """FAQ/아코디언 패턴 감지"""
    patterns = {
        'details_tags': [],
        'aria_expanded_false': [],
        'faq_without_active': [],
        'ac_panel_without_show': [],
        'display_none_answers': []
    }
    
    # 패턴 1: <details> 태그 (open 속성 없음)
    details_pattern = r'<details\s+[^>]*>|<details>'
    for match in re.finditer(details_pattern, content, re.IGNORECASE):
        if 'open' not in match.group(0).lower():
            patterns['details_tags'].append(match.start())
    
    # 패턴 2: aria-expanded="false"
    aria_false_pattern = r'aria-expanded\s*=\s*["\']false["\']'
    for match in re.finditer(aria_false_pattern, content, re.IGNORECASE):
        patterns['aria_expanded_false'].append(match.start())
    
    # 패턴 3: .kst-faq 또는 .faq 클래스가 있지만 .kst-active 또는 .active가 없는 경우
    # (단, FAQ 섹션 내부에서만)
    faq_section_pattern = r'(<div[^>]*class\s*=\s*["\'][^"\']*faq[^"\']*["\'][^>]*>)(?!.*active)'
    for match in re.finditer(faq_section_pattern, content, re.IGNORECASE):
        if 'kst-active' not in match.group(0).lower() and 'active' not in match.group(0).lower():
            patterns['faq_without_active'].append(match.start())
    
    # 패턴 4: .kst-ac-panel 또는 .ac-panel이 있지만 .kst-show 또는 .show가 없는 경우
    ac_panel_pattern = r'(<div[^>]*class\s*=\s*["\'][^"\']*ac-panel[^"\']*["\'][^>]*>)(?!.*show)'
    for match in re.finditer(ac_panel_pattern, content, re.IGNORECASE):
        if 'kst-show' not in match.group(0).lower() and 'show' not in match.group(0).lower():
            patterns['ac_panel_without_show'].append(match.start())
    
    return patterns

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

def fix_faq_active(content: str) -> Tuple[str, int]:
    """faq 클래스에 active 클래스 추가 (answer가 아닌 경우만)"""
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
    
    # 잘못 추가된 answer의 active 제거
    content = re.sub(
        r'class\s*=\s*["\']([^"\']*faq-answer[^"\']*)\s+kst-active["\']',
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
        
        # 패턴 감지
        patterns = detect_accordion_patterns(content)
        
        # 수정 적용
        stats = {
            'details': 0,
            'aria_expanded': 0,
            'ac_panel': 0,
            'faq_active': 0
        }
        
        content, stats['details'] = fix_details_tags(content)
        content, stats['aria_expanded'] = fix_aria_expanded(content)
        content, stats['ac_panel'] = fix_ac_panel_show(content)
        content, stats['faq_active'] = fix_faq_active(content)
        
        # 변경사항이 있으면 저장
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {
                'modified': True,
                'stats': stats,
                'patterns_detected': patterns
            }
        else:
            return {
                'modified': False,
                'stats': stats,
                'patterns_detected': patterns
            }
    
    except Exception as e:
        return {'modified': False, 'error': str(e)}

def main():
    """메인 함수"""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    html_files = find_html_files(root_dir)
    
    print(f"📁 총 {len(html_files)}개의 HTML 파일을 찾았습니다.\n")
    print("=" * 70)
    print("FAQ/아코디언 패턴 포괄 분석 및 수정 중...")
    print("=" * 70)
    
    total_stats = {
        'details': 0,
        'aria_expanded': 0,
        'ac_panel': 0,
        'faq_active': 0
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
            if stats['faq_active'] > 0:
                changes.append(f"faq-active: {stats['faq_active']}")
            
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
    print(f"  - faq-active: {total_stats['faq_active']}개")
    
    if error_files:
        print(f"\n⚠️ 오류 발생 파일:")
        for file_path, error in error_files:
            print(f"  - {os.path.basename(file_path)}: {error}")

if __name__ == '__main__':
    main()

