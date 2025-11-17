# 아코디언/FAQ 패턴 분석 결과

## 📋 발견된 패턴 요약

이 리포지토리에서 발견된 드롭다운/아코디언/FAQ 컴포넌트 패턴은 총 **4가지**입니다.

---

## 1️⃣ `<details><summary>` 태그 패턴

### 구조
```html
<details>
  <summary>질문</summary>
  <div class="qa">답변</div>
</details>
```

### 사용 파일 예시
- `a01-exoxe-product-page.html`
- `a43-super-v-line-max-description.html`
- `a48-white-lumi-description.html`

### 현재 상태
- **기본 상태**: 접힘 (collapsed)
- **접힘/펼침 제어**: HTML5 네이티브 `open` 속성

### 수정 방법
- `<details>` 태그에 `open` 속성 추가
- 예: `<details>` → `<details open>`

### CSS 영향
- CSS는 변경 불필요 (브라우저 네이티브 동작)

---

## 2️⃣ `.kst-ac-item` + `aria-expanded` + `.kst-show` 패턴

### 구조
```html
<div class="kst-ac-item" aria-expanded="false">
  <button class="kst-ac-button" aria-controls="kst-ac1" aria-expanded="false">
    질문 <span>＋</span>
  </button>
  <div id="kst-ac1" class="kst-ac-panel">답변</div>
</div>
```

### 사용 파일 예시
- `a32-selatox-10.html`
- `a47-wells_line_contouring_serum.html`
- `a45-velash_exo_plus_shopify.html`
- `a37-pilla-plla-shopify-description.html`
- `complete-shopify/` 내 다수 파일

### 현재 상태
- **기본 상태**: 접힘
- **접힘/펼침 제어**: 
  - `aria-expanded="false"` → `aria-expanded="true"`
  - `.kst-ac-panel`에 `.kst-show` 클래스 추가 필요
  - JavaScript로 `max-height` 토글

### 수정 방법
1. `aria-expanded="false"` → `aria-expanded="true"` 변경
2. `.kst-ac-panel`에 `kst-show` 클래스 추가
3. 버튼의 `span` 텍스트 `＋` → `−` 변경 (선택사항)

### CSS 확인
```css
.kst-ac-panel {
  max-height: 0;
  overflow: hidden;
  transition: max-height .3s ease;
}

.kst-ac-panel.kst-show {
  max-height: 500px;
  padding: 14px 16px;
}
```

---

## 3️⃣ `.kst-faq` + `.kst-active` 패턴 (a06 등)

### 구조
```html
<div class="kst-faq">
  <button class="kst-faq-question" onclick="kstToggleFAQ(this)">
    <span>질문</span>
    <span class="kst-faq-icon">+</span>
  </button>
  <div class="kst-faq-answer">답변</div>
</div>
```

### 사용 파일 예시
- `a06-fiola-eyebag-shopify.html`
- `a16-lipovela_v_shopify_description.html`

### 현재 상태
- **기본 상태**: 접힘
- **접힘/펼침 제어**: 
  - `.kst-faq`에 `.kst-active` 클래스 추가
  - JavaScript로 `display` 토글

### 수정 방법
- `.kst-faq`에 `kst-active` 클래스 추가
- 예: `<div class="kst-faq">` → `<div class="kst-faq kst-active">`

### CSS 확인
```css
.kst-faq-answer {
  display: none;
}

.kst-faq.kst-active .kst-faq-answer {
  display: block;
}
```

---

## 4️⃣ `.kst-faq-item` 단순 표시 패턴

### 구조
```html
<div class="kst-faq-item">
  <div class="kst-faq-question">질문</div>
  <div class="kst-faq-answer">답변</div>
</div>
```

### 사용 파일 예시
- `a31-selastin-tox-description.html`

### 현재 상태
- **기본 상태**: 항상 표시 (접힘 없음)
- **접힘/펼침 제어**: 없음

### 수정 방법
- **변경 불필요** (이미 항상 표시됨)

---

## 🔧 수정 전략

### 안전성 고려사항
1. **JavaScript 동작 유지**: 모든 클릭 이벤트 핸들러는 그대로 유지
2. **CSS 충돌 방지**: 기존 CSS 규칙과 호환되도록 수정
3. **접근성 유지**: `aria-expanded` 속성은 올바르게 설정

### 수정 우선순위
1. `<details>` 태그 → 가장 간단하고 안전
2. `.kst-ac-item` 패턴 → 가장 많이 사용됨
3. `.kst-faq` 패턴 → 일부 파일에서 사용

---

## 📊 예상 영향 범위

- **총 HTML 파일**: 약 124개
- **수정 대상 파일**: 약 50-70개 (FAQ/아코디언이 있는 파일)
- **수정 안전성**: 높음 (기본값만 변경, JS 로직 유지)

---

## ✅ 검증 방법

수정 후 다음을 확인:
1. 브라우저에서 페이지 로드 시 FAQ/아코디언이 펼쳐져 있는지 확인
2. 클릭 시 접힘/펼침 동작이 정상 작동하는지 확인
3. JavaScript 콘솔에 에러가 없는지 확인

