---
name: theology-translator
description: >
  Translates theological texts (DE/EN → KO) through an orchestrator-led,
  role-isolated team loop — lossless Drafter, adversarial Red-Team Auditor,
  and Stylist under a PM quality gate with a 70% token-ratio guard; Author
  Mode adds an Exegetical Analyst for primary texts (Barth, Bonhoeffer).
  Use when the user asks to translate theological literature, lectures, or
  primary sources with academic fidelity.
  키워드: 신학 번역, 원전 번역, 강연 번역, 번역 감수
version: 6.0.0
status: active
author: MS_Dev
triggers:
  - "#번역"
  - "#theology-translator"
  - "신학 번역해줘"
  - "이 원전 번역해줘"
references_path: ./references
---

# 🌐 Theology Translator (역할 격리 신학 번역 파이프라인)

신학 텍스트를 페르소나 완전 격리(Role Isolation) 체제로 번역합니다. 한 에이전트가
초벌·감수·윤문을 겸하지 않습니다 — 각 역할의 규칙은 분리된 reference가 정본입니다.

## Phase 0 — 가드레일

- [gotchas.md](./references/gotchas.md)를 읽고 알려진 번역 함정을 확인합니다.
- **TRE 용어 정책(워크스페이스 헌법)**: 초벌·사유 생성 단계에서 `tre_terms.csv`를
  강제 매핑하지 않습니다. 최종 검수·출판 직전에만 참조 필터로 사용합니다
  (→ `.skills/theology-terminology-linter`).
- 원문 샘플링으로 **Project Style Guide + Dynamic Glossary**를 먼저 확정합니다
  (스키마: [templates/style_guide_schema.json](./templates/style_guide_schema.json)).

## Phase 1-4 — 번역 루프 (정본: [translation-loop.md](./references/translation-loop.md))

| 역할 | 임무 | 핵심 규칙 |
|---|---|---|
| **Role 0 — Orchestrator(PM)** | 워크로드 분할, 품질 게이트 | 단락(¶) 밀도 기준 분할, Token Ratio Guard(70%) 검문 |
| **Agent 1 — Drafter** | 무손실 초안 | 가독성 무시, 모든 성분 전사, `[¶N]` ID 필수 |
| **Agent 2 — Red-Team Auditor** | 오류·누락 색출 | 직접 수정 금지, 리포트만. Anti-Summary 3곳 이상 지적 |
| **Agent 3 — Stylist** | 최종 윤문 | **원문 참조 금지**, 정보량 보존, 스타일 자가 진단 |

- **Author Mode** (1차 문헌 — 바르트, 본회퍼 등): 위 루프 앞에 **Exegetical Analyst**가
  다의어(Geist, Aufhebung 등)의 저자·시대별 정의를 스캔해 용어 주입 지침을 생성합니다.
  정본: [author-mode-roles.md](./references/author-mode-roles.md),
  [payload-schema.md](./references/payload-schema.md)
- **YouTube 강연 번역**: [yt_lecture_protocol.md](./references/yt_lecture_protocol.md) +
  [templates/yt_lecture_template.md](./templates/yt_lecture_template.md) 규격을 따릅니다.

## Phase 5 — 품질 게이트 (Quality Gate)

- PM이 단계별 산출물을 종합 검토해 원문과의 등가성(Equivalence)을 확인하고,
  [templates/pm_quality_report.md](./templates/pm_quality_report.md) 양식으로 보고합니다.
- 검문 항목: ¶ 개수 일치, Token Ratio ≥ 70%, 용어집 위반 0건, 신명(Divine Names) 일관성.
- 기계적 검문 (PASS 시 종료코드 0):
  ```bash
  python3 scripts/translator_audit.py --source 원문.md --draft 번역.md \
    [--glossary glossary.json] [--min-ratio 0.7]
  ```
  교차 문자체계(라틴→한글)는 단어수 기반 정보량 비율로 자동 보정됩니다.

## 검증·보고

- 최종 보고에 사용한 모드(기본/Author/YT), 스타일 가이드 요지, 품질 게이트 결과를
  포함합니다. 검증하지 못한 항목은 그렇다고 말합니다.
- 상태 표기 용어는 [status-terminology.md](./references/status-terminology.md)를 따릅니다.
