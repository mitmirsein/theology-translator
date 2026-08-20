#!/usr/bin/env python3
"""theology-translator Phase 5 기계적 품질 게이트.

deps: Python 3.9+ stdlib only.
실행: python3 translator_audit.py --source 원문.md --draft 번역.md
      [--glossary glossary.json] [--min-ratio 0.7] [--json]

검문 항목 (SKILL.md Phase 5):
  1. ¶ 마커 정합 — 번역문의 [¶N] 마커가 연속·중복 없이 존재하는가
  2. Token Ratio Guard — 정보량 보존 (기본: 공백 제외 문자수 비율 ≥ 0.7)
  3. 용어집 위반 — glossary.json {원어: 필수 역어}의 강제 매핑 검사
  4. 신명(Divine Names) 일관성 — 하나님/하느님 등 혼용 검출
종료코드: 0 = PASS, 1 = FAIL
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MARKER_RE = re.compile(r"\[¶(\d+)\]")
DIVINE_VARIANTS = [("하나님", "하느님"), ("여호와", "야훼")]


def char_count(text: str) -> int:
    return len(re.sub(r"\s", "", text))


CJK_RE = re.compile(r"[가-힣一-鿿぀-ヿ]")


def volume_ratio(source: str, draft: str, cjk_factor: float = 2.0) -> tuple[float, str]:
    """정보량 보존 비율. 라틴 원문 → 한글 번역은 '원문 단어수 × factor' 대비
    한글 음절수로 비교한다 (한국어가 문자 단위로 훨씬 조밀하므로 단순 문자비는 왜곡됨).
    같은 문자체계끼리는 공백 제외 문자수 비율을 쓴다."""
    src_cjk = len(CJK_RE.findall(source))
    drf_cjk = len(CJK_RE.findall(draft))
    src_chars = char_count(source)
    if drf_cjk > src_cjk * 2 and src_chars and src_cjk / src_chars < 0.2:
        src_words = len(source.split())
        expected = src_words * cjk_factor
        ratio = drf_cjk / expected if expected else 0.0
        return ratio, f"한글 {drf_cjk}자 / 기대치 {expected:.0f} (원문 {src_words}단어 × {cjk_factor})"
    drf_chars = char_count(draft)
    ratio = drf_chars / src_chars if src_chars else 0.0
    return ratio, f"문자수 {src_chars} → {drf_chars}"


def audit(source: str, draft: str, glossary: dict, min_ratio: float) -> dict:
    checks = []

    # 1. ¶ 마커 정합
    markers = [int(m) for m in MARKER_RE.findall(draft)]
    if not markers:
        checks.append(("paragraph_markers", False, "번역문에 [¶N] 마커가 없음 (Drafter 규칙 위반)"))
    else:
        dups = sorted({m for m in markers if markers.count(m) > 1})
        missing = sorted(set(range(min(markers), max(markers) + 1)) - set(markers))
        ok = not dups and not missing
        detail = f"마커 {len(markers)}개 (¶{min(markers)}–¶{max(markers)})"
        if dups:
            detail += f"; 중복 {dups[:5]}"
        if missing:
            detail += f"; 누락 {missing[:5]}"
        checks.append(("paragraph_markers", ok, detail))

    # 2. Token Ratio Guard (문자체계 인지형 정보량 비율)
    ratio, basis = volume_ratio(source, MARKER_RE.sub("", draft))
    checks.append(("token_ratio", ratio >= min_ratio,
                   f"비율 {ratio:.2f} ({basis}, 기준 ≥ {min_ratio})"))

    # 3. 용어집 위반
    violations = []
    for term, required in glossary.items():
        if term in source and required not in draft:
            violations.append(f"'{term}' → '{required}' 미사용")
    checks.append(("glossary", not violations,
                   "; ".join(violations[:5]) if violations else f"용어집 {len(glossary)}건 준수"))

    # 4. 신명 일관성
    mixed = [f"{a}/{b} 혼용" for a, b in DIVINE_VARIANTS if a in draft and b in draft]
    checks.append(("divine_names", not mixed, "; ".join(mixed) if mixed else "일관"))

    return {
        "pass": all(ok for _, ok, _ in checks),
        "ratio": round(ratio, 3),
        "checks": [{"name": n, "ok": ok, "detail": d} for n, ok, d in checks],
    }


def main():
    ap = argparse.ArgumentParser(description="theology-translator 품질 게이트")
    ap.add_argument("--source", required=True, help="원문 파일")
    ap.add_argument("--draft", required=True, help="번역문 파일")
    ap.add_argument("--glossary", help="용어집 JSON {원어: 필수 역어}")
    ap.add_argument("--min-ratio", type=float, default=0.7)
    ap.add_argument("--json", action="store_true", help="JSON 출력")
    args = ap.parse_args()

    source = Path(args.source).read_text(encoding="utf-8")
    draft = Path(args.draft).read_text(encoding="utf-8")
    glossary = json.loads(Path(args.glossary).read_text(encoding="utf-8")) if args.glossary else {}

    result = audit(source, draft, glossary, args.min_ratio)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    else:
        print(f"{'✅ PASS' if result['pass'] else '❌ FAIL'} — translator_audit")
        for c in result["checks"]:
            print(f"  [{'OK' if c['ok'] else 'NG'}] {c['name']}: {c['detail']}")
    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
