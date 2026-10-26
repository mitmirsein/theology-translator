# 🌐 Theology Translator (신학 원전 고정밀 번역 파이프라인)

신학 문헌, 학술 강연, 원전(1차 사료: 바르트, 본회퍼 등)을 무손실·고정밀로 번역하기 위한 **역할 격리**(Role Isolation) 기반 다중에이전트 번역 파이프라인이다.

단일 에이전트 번역의 고질적 문제인 **임의 요약**(Summary Trap), **신학적 편향**(Theological Drift), **만연체 해설화**(Over-Interpretation)를 구조적으로 차단한다.

---

## 🎯 핵심 설계 원칙

1. **페르소나 완전 격리**(Role Isolation)
   - 초벌 번역, 적대적 감사, 문체 교정의 역할을 완전히 분리한다.
   - 문체 교정관(Stylist)은 원문을 일체 보지 않고 정보량만 보존하며 한국어 문장을 재조립한다.
2. **무손실 충실도 보장**(Lossless Fidelity Harness)
   - 가독성을 이유로 원문의 세부 예시, 부연 설명, 반복 강조를 축소하거나 생략하는 것을 엄격히 금지한다.
   - 단락 단위로 `[¶N]` 고유 식별자를 부여하여 원문과 번역문의 1:1 매핑을 강제한다.
3. **적대적 감사 및 요약 방지 지뢰선**(Anti-Summary Tripwire)
   - 감사관(Red-Team Auditor)은 번역문을 직접 수정하지 않고 누락 구간을 적대적으로 색출한다.
   - `요약하면`, `핵심은`, `저자는 주장한다` 등 임의 해설 패턴 발생 시 즉시 반려한다.
4. **기계적 품질 게이트**(Mechanical Quality Gate)
   - 파이썬 기반 감사 스크립트([`scripts/translator_audit.py`](scripts/translator_audit.py))로 단락 마커, 정보량 비율(Token Ratio), 용어집 준수, 신명 일관성을 기계적으로 검증한다.

---

## 🔄 파이프라인 구조

```
[Phase 0] 프로젝트 가이드라인 & Dynamic Glossary 확정
                     ↓
[Role 0: Orchestrator (PM)]  ─── 단락(¶) 밀도 기준 워크로드 분할
                     ↓
[Agent 1: The Drafter]       ─── 무손실 전사 초안 (가독성 배제, [¶N] 마커)
                     ↓
[Agent 2: Red-Team Auditor]  ─── 적대적 대조 감사 (오류·누락 색출, 의미 단위 보존 점검)
                     ↓
[Agent 3: The Stylist]       ─── 독립 윤문 (원문 참조 금지, 정보량 100% 보존)
                     ↓
[Phase 5: Mechanical Gate]   ─── translator_audit.py 자동 검문 (PASS 시 최종 승인)
```

### 특화 모드 (Specialized Modes)

- **Author Mode**(1차 원전 번역): 바르트(Karl Barth), 본회퍼(Dietrich Bonhoeffer) 등 고난도 원전 번역 시 **Exegetical Analyst**가 선행하여 다의어(Geist, Wort, Aufhebung 등)의 시대·저자별 정의를 스캔하고 용어 주입 지침을 생성한다.
- **YouTube & 강연 자막 번역 SOP**: VTT 자막 소스 확보 → 원어 힐링 및 대조 게이트 → 단락 동수 검수 → Red-Team Pass → Receiver Pass → 글로서리 안치로 이어지는 표준 공정을 제공한다.

---

## 📂 디렉터리 구성

```text
theology-translator/
├── SKILL.md                          # 에이전트 스킬 정의서 (규격 표준)
├── LICENSE                           # MIT License
├── README.md                         # 프로젝트 안내서
├── references/                       # 상세 실행 규칙 및 프로토콜
│   ├── author-mode-roles.md          # Author Mode 전용 역할 정의
│   ├── gotchas.md                    # 신학 번역 함정 및 Anti-Summary 프로토콜
│   ├── payload-schema.md             # Author Mode 입력 JSON 스키마
│   ├── source-healing.md             # 자막·녹취 원어 힐링 및 원본 대조 지침
│   ├── status-terminology.md         # 내부 상태 코드 및 용어 정책
│   ├── translation-loop.md           # 4단계 번역 루프 상세 규정
│   └── yt_lecture_protocol.md        # YouTube/강연 번역 표준 공정(SOP)
├── scripts/                          # 자동화 및 검증 도구
│   └── translator_audit.py           # 기계적 품질 게이트 검증 스크립트
└── templates/                        # 표준 보고서 및 산출물 템플릿
    ├── pm_quality_report.md          # PM 품질 게이트 평가 보고서 양식
    ├── style_guide_schema.json       # 프로젝트 스타일 가이드 JSON 스키마
    └── yt_lecture_template.md        # 강연 번역 산출물 마크다운 템플릿
```

---

## 🛠️ 기계적 품질 게이트 사용법

별도 외부 라이브러리 설치 없이 Python 3.9+ 표준 라이브러리 환경에서 즉시 실행할 수 있다.

```bash
# 기본 검문 실행
python3 scripts/translator_audit.py --source 원문.md --draft 번역문.md

# 용어집 및 최소 정보량 비율 지정
python3 scripts/translator_audit.py \
  --source 원문.md \
  --draft 번역문.md \
  --glossary glossary.json \
  --min-ratio 0.7

# JSON 결과 출력
python3 scripts/translator_audit.py --source 원문.md --draft 번역문.md --json
```

### 검문 항목
1. **단락 마커 정합 및 동수**(`paragraph_markers`): 원문과 번역문의 `[¶N]` 마커 일치(Parity) 및 번역문 내 연속성·누락·중복 여부
2. **정보량 보존율**(`token_ratio`): 한글 음절수와 원문 단어수 기반 정보량 보존 비율 (기준: ≥ 0.70)
3. **용어집 준수**(`glossary`): 지정된 용어집 매핑 준수 여부
4. **신명 일관성**(`divine_names`): 하나님/하느님, 여호와/야훼 혼용 검출

---

## 📦 Claude Code / Antigravity 스킬 등록

에이전트 환경의 스킬 디렉터리에 클론하거나 심볼릭 링크를 걸어 즉시 사용할 수 있다.

```bash
# 스킬 저장소로 클론
git clone https://github.com/mitmirsein/theology-translator.git ~/.skills/theology-translator
```

---

## 📜 라이선스

이 프로젝트는 [MIT License](LICENSE)에 따라 배포된다.
