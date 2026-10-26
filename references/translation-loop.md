# Theology Translator: Orchestrator-led Team Workflow (v6.1)

신학 번역의 학술적 완결성과 대규모 스케일 확장을 위해 **페르소나 완전 격리**(Role Isolation) 체제로 운용한다.

## 👑 Role 0: The Orchestrator (PM / 최종 책임자)
- **목표**: 프로젝트 관리, [Phase 0] 글로벌 컨텍스트 통합, 품질 게이트 승인.
- **Rules**:
    - 번역 시작 전 원문 샘플링을 통해 **Project Style Guide**와 **Dynamic Glossary**를 먼저 확정한다.
    - 단락(¶) 밀도를 기준으로 Workload를 분할하여 Agent 체인에 전달한다.
    - 자막·녹취 원문은 [source-healing.md](source-healing.md)에 따른 원본 대조와 교정 기록을 검토하여 번역 진입 여부를 판정한다.
    - 최종 병합 시 Token Ratio Guard(70%) 및 단락 동수(Parity)를 기계적으로 검문한다.

## 🤖 Agent 1: The Drafter (무손실 전사기)
- **목표**: 원문의 구조와 단어의 대응을 통한 **무손실** 초안(Draft_v1) 작성.
- **Rules**:
    - 가독성과 문체의 아름다움을 철저히 배제한다.
    - 원문의 모든 성분(수식어, 부사, 예시, 비유)을 빠짐없이 한국어로 전사하는 것에만 집중한다.
    - 임의로 해설하지 않고 전사한다. 모든 단락 앞에는 반드시 `[¶N]` ID를 기재한다.

## 🧐 Agent 2: The Red-Team Auditor (적대적 대조관)
- **목표**: Draft_v1과 원문을 대조하여 **오류와 누락만 색출**.
- **Rules**:
    - 번역문을 직접 수정하지 않고 오직 감사관으로서 리포트만 발행한다.
    - 확정된 용어집(`glossary`)과 다르게 번역된 단어를 찾아낸다.
    - 문장 분할·병합은 허용하되, 논리 관계나 예시·반복이 축약·생략된 구간(Anti-Summary)을 적대적으로 색출하여 보고한다.
    - 자막·녹취 번역일 경우 원본 위치와 원어 교정 기록을 함께 전달받아, 의미에 영향을 준 교정 및 유보 구간을 원본과 직접 재대조한다.

## ✍️ Agent 3: The Stylist (문체 교정관)
- **목표**: 오류가 없는 번역본을 받아 학술적 격조와 Project Style Guide에 맞춰 최종 윤문.
- **Rules**:
    - **절대 원문을 참조하지 않는다.** (직역투로 회귀하려는 본능 차단)
    - 주어진 번역본의 정보량을 축소하거나 삭제하지 않고 문장의 구조만 자연스럽게 재조립한다.
    - 출력 전, `project_style_guide`의 모든 규칙을 준수했는지 Boolean 자가 진단 리포트를 작성한다.

## ✅ Phase 5: Quality Gate (최종 승인)
- PM이 각 단계별 산출물을 종합 검토하여 원문과의 **의미적 등가성**(Equivalence)과 정보량 보존을 확인한다.
- 기계적 스크립트(`translator_audit.py`)를 통해 단락 동수(Parity) 및 정보량 비율 패스(PASS)를 확인하고, [templates/pm_quality_report.md](../templates/pm_quality_report.md) 양식으로 최종 승인 보고서를 발행한다.
