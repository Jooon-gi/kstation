# FAQ/아코디언 패턴 상세 분석

## 📋 1단계: 패턴 탐색 및 요약

### 패턴 A: `<details><summary>` HTML5 네이티브 패턴

#### HTML 구조 예시
```html
<div class="accordion">
  <details>
    <summary>질문</summary>
    <div class="qa">답변</div>
  </details>
</div>
```

#### 펼쳐진 상태 표현
- **속성**: `<details open>`
- **초기 접힌 상태**: `open` 속성 없음

#### 사용 파일
- `a01-exoxe-product-page.html` ✅ (이미 수정됨)
- `a43-super-v-line-max-description.html` ✅ (이미 수정됨)
- `a48-white-lumi-description.html` ✅ (이미 수정됨)

---

### 패턴 B: `.kst-ac-item` + `aria-expanded` + `.kst-show` 패턴

#### HTML 구조 예시
```html
<div class="kst-ac-item" aria-expanded="false">
  <button class="kst-ac-button" aria-controls="kst-ac1" aria-expanded="false">
    질문 <span>＋</span>
  </button>
  <div id="kst-ac1" class="kst-ac-panel">답변</div>
</div>
```

#### 펼쳐진 상태 표현
- **속성**: `aria-expanded="true"` (item과 button 모두)
- **클래스**: `.kst-ac-panel`에 `.kst-show` 클래스
- **CSS**: 
  ```css
  .kst-ac-panel {
    max-height: 0;
    overflow: hidden;
  }
  .kst-ac-panel.kst-show {
    max-height: 500px;
    padding: 14px 16px;
  }
  ```

#### 초기 접힌 상태
- `aria-expanded="false"` (기본값)
- `.kst-show` 클래스 없음
- `max-height: 0`으로 숨김

#### JavaScript 동작
```javascript
// 클릭 시 aria-expanded 토글 및 .kst-show 클래스 토글
item.setAttribute('aria-expanded', String(!isOpen));
panel.classList.toggle('kst-show');
```

#### 사용 파일
- `a32-selatox-10.html` ✅ (이미 수정됨)
- `a47-wells_line_contouring_serum.html` ✅ (이미 수정됨)
- `a45-velash_exo_plus_shopify.html` ✅ (이미 수정됨)
- `a37-pilla-plla-shopify-description.html` ✅ (이미 수정됨)
- `index.html` ✅ (이미 수정됨)

---

### 패턴 C: `.kst-faq` + `.kst-active` 패턴 (a06 스타일)

#### HTML 구조 예시
```html
<div class="kst-faq">
  <button class="kst-faq-question" onclick="kstToggleFAQ(this)">
    <span>질문</span>
    <span class="kst-faq-icon">+</span>
  </button>
  <div class="kst-faq-answer">답변</div>
</div>
```

#### 펼쳐진 상태 표현
- **클래스**: `.kst-faq`에 `.kst-active` 클래스
- **CSS**:
  ```css
  .kst-faq-answer {
    display: none;
  }
  .kst-faq.kst-active .kst-faq-answer {
    display: block;
  }
  ```

#### 초기 접힌 상태
- `.kst-active` 클래스 없음
- `display: none`으로 숨김

#### JavaScript 동작
```javascript
function kstToggleFAQ(button) {
  const faqItem = button.parentElement;
  const isActive = faqItem.classList.contains('kst-active');
  
  // 모든 FAQ 닫기
  document.querySelectorAll('.kst-faq').forEach(item => {
    item.classList.remove('kst-active');
  });
  
  // 클릭한 항목 열기
  if (!isActive) {
    faqItem.classList.add('kst-active');
  }
}
```

#### 사용 파일
- `a06-fiola-eyebag-shopify.html` ✅ (이미 수정됨)
- `a16-lipovela_v_shopify_description.html` ✅ (이미 수정됨)
- `a11-lacto-exo-colla-lxc-product-description.html` ✅ (이미 수정됨)
- `a17-luscilipo-description.html` ✅ (이미 수정됨)

---

### 패턴 D: `.kst-faq-item` 단순 표시 패턴 (a31 스타일)

#### HTML 구조 예시
```html
<div class="kst-faq-item">
  <div class="kst-faq-question">질문</div>
  <div class="kst-faq-answer">답변</div>
</div>
```

#### 펼쳐진 상태 표현
- **항상 표시됨** (접힘 기능 없음)
- CSS에 숨김 규칙 없음

#### 초기 상태
- 이미 항상 표시됨
- **수정 불필요**

#### 사용 파일
- `a31-selastin-tox-description.html` (수정 불필요)

---

### 패턴 E: `.kst-faq-section` + `.kst-faq-item` + `.kst-active` 패턴 (complete-shopify/17 스타일)

#### HTML 구조 예시
```html
<div class="kst-faq-section kst-active">
  <div class="kst-faq-item kst-active">
    <button class="kst-faq-question" onclick="kstToggleFAQ(this)">
      질문
      <span class="kst-faq-toggle">+</span>
    </button>
    <div class="kst-faq-answer">답변</div>
  </div>
</div>
```

#### 펼쳐진 상태 표현
- **클래스**: `.kst-faq-item`에 `.kst-active` 클래스
- CSS는 패턴 C와 유사할 것으로 예상

#### 사용 파일
- `complete-shopify/17-fiola-s-product-description.html` ✅ (이미 수정됨)

---

## 📊 패턴별 수정 전략 요약

| 패턴 | 펼쳐진 상태 표현 | 수정 방법 | 상태 |
|------|----------------|----------|------|
| A: `<details>` | `open` 속성 | `<details>` → `<details open>` | ✅ 완료 |
| B: `.kst-ac-item` | `aria-expanded="true"` + `.kst-show` | `aria-expanded="false"` → `"true"`, `.kst-show` 추가 | ✅ 완료 |
| C: `.kst-faq` | `.kst-active` 클래스 | `.kst-faq` → `.kst-faq kst-active` | ✅ 완료 |
| D: `.kst-faq-item` | 항상 표시 | 수정 불필요 | ✅ 확인 |
| E: `.kst-faq-section` | `.kst-active` 클래스 | `.kst-faq-item` → `.kst-faq-item kst-active` | ✅ 완료 |

---

## 🔍 추가 확인 필요 사항

다음 파일들을 확인하여 다른 패턴이 있는지 검증 필요:
1. 아직 확인하지 않은 파일들
2. 다른 네이밍 컨벤션을 사용하는 파일들
3. 커스텀 JavaScript를 사용하는 파일들

