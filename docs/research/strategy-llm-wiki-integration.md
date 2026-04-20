# Strategy: LLM Wiki Integration into claude-meta-autoagent

> 전략 수립 및 보고서 — LLM Wiki 패턴을 현재 프로젝트에 적용하기 위한 분석과 실행 계획.
> Date: 2026-04-14

---

## 1. 현재 상태 분석

### 프로젝트의 지식 관리 현황

| 계층 | 현재 방식 | 형태 | 한계 |
|------|----------|------|------|
| **Cross-run Learning** | JSONL append-only | `strategies.jsonl` (7건), `anti-patterns.jsonl` (1건) | 플랫 구조, 교차 참조 없음, 모순 미감지, 스케일 한계 |
| **Scorer Evolution** | JSONL append-only | `scorer-evolution.jsonl` (4건) | 축적만 되고 통합/분석 없음 |
| **Reflexion** | attempts/ JSONL | `refine-*.jsonl` (4건) | 세션 내 활용만, 장기 지식화 안 됨 |
| **Documentation** | 정적 마크다운 | `docs/` (3 core + 5 research) | 수동 유지, 자동 업데이트 없음 |
| **Meta-Evolution 관찰** | 일회성 로그 | `/tmp/agent.log`, git log | 관찰 결과 축적 없음, 세션 종료 시 소멸 |

### 핵심 문제

1. **JSONL의 구조적 한계**: 전략 S-1이 안티패턴 A-1과 관련되지만, 교차 참조 없음.
   7개 전략이 각각 독립적으로 존재 — 패턴 간 관계 파악 불가.
2. **관찰 지식의 소멸**: Meta-Evolution 관찰 결과가 `/tmp/agent.log`에만 존재하고
   세션 종료 시 사라짐. 동일한 문제를 반복 진단하는 원인.
3. **Scorer evolution의 미활용**: 기록만 되고, "어떤 체크를 왜 추가했는지" 맥락 부재.
4. **문서 정체**: `docs/`가 수동 업데이트. 새로운 전략이 축적되어도 문서 반영 안 됨.

---

## 2. 적용 전략: 3-Phase Approach

### 아키텍처 비전

```
┌──────────────────── claude-meta-autoagent ────────────────────┐
│                                                                │
│  Layer 1: ROOT — Meta-Evolution                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ .claude/                                                │   │
│  │ .refine/score.sh (ROOT scorer)                          │   │
│  │                                                         │   │
│  │ knowledge/              ◄── NEW: LLM Wiki               │   │
│  │ ├── raw/                    (Meta-Evolution 지식 축적)   │   │
│  │ │   ├── observations/       관찰 로그 (immutable)       │   │
│  │ │   ├── reflexions/         반성 기록 (immutable)       │   │
│  │ │   └── external/           외부 리서치 (immutable)     │   │
│  │ ├── wiki/                                               │   │
│  │ │   ├── index.md            마스터 카탈로그              │   │
│  │ │   ├── log.md              작업 연대기                 │   │
│  │ │   ├── strategies/         성공 전략 페이지            │   │
│  │ │   ├── anti-patterns/      실패 패턴 페이지            │   │
│  │ │   ├── scorer-insights/    스코러 진화 인사이트        │   │
│  │ │   └── system-evolution/   시스템 개선 이력            │   │
│  │ └── schema.md               위키 운영 규칙              │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                │
│  Layer 2: Sub-project                                          │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ .claude/agent-memory/   (기존 JSONL — Phase 2에서 전환) │   │
│  │ .refine/score.sh                                        │   │
│  │ [project code]                                          │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

---

### Phase 1: `/wiki` Skill — 사용자 대면 기능 추가

**목표**: 프로젝트 사용자가 자기 프로젝트에 LLM Wiki를 적용할 수 있는 skill 제공.

**근거**: claude-meta-autoagent의 핵심 가치는 "범용 자율 에이전트 시스템". autoresearch가
코드 진화를 담당한다면, LLM Wiki는 **지식 진화**를 담당. 두 패턴이 보완 관계.

**산출물**:
```
.claude/skills/wiki/
├── SKILL.md          # /wiki ingest, /wiki query, /wiki lint 명세
└── schema-template.md  # 사용자 프로젝트용 기본 스키마
```

**Skill 구조**:
| 명령 | 동작 |
|------|------|
| `/wiki init` | 프로젝트에 `knowledge/raw/`, `wiki/`, `schema.md` 생성 |
| `/wiki ingest <source>` | 소스 → 위키 페이지 cascade 업데이트 |
| `/wiki query <question>` | 위키 검색 → 답변 합성 → 선택적 페이지 생성 |
| `/wiki lint` | 모순, 고아 페이지, 오래된 주장, 공백 검사 |

**범위**: 이 phase에서는 `/refine`과 `/wiki`가 독립적으로 운영.
사용자가 원하면 프로젝트에 둘 다 적용 가능하지만 연동은 아직 없음.

**Scorer 항목 추가** (ROOT scorer):
```
W1: /wiki skill 존재
W2: schema-template.md 존재
W3: SKILL.md에 init/ingest/query/lint 4개 operation 정의
```

**위험**: 낮음. 기존 기능에 영향 없이 skill만 추가.

---

### Phase 2: Agent-Memory → Wiki 구조 전환

**목표**: 현재 JSONL 기반 cross-run learning을 위키 구조로 진화.

**근거**: 현재 학습 데이터의 한계:

| 문제 | JSONL 현재 | Wiki 전환 후 |
|------|-----------|-------------|
| 전략 S-1 ↔ 안티패턴 A-1 관계 | 별도 파일, 링크 없음 | `[[A-1-pipefail]]` wikilink로 교차 참조 |
| "sanitizer 전략은 이미 3번 성공" | 파일 전체 로드 후 세어야 함 | `strategies/sanitizer.md`에 이력 축적 |
| 모순된 전략 감지 | 불가 | Lint에서 자동 플래그 |
| 스코러 체크 추가 이유 | `scorer-evolution.jsonl`에 1줄 | `scorer-insights/F10-security.md`에 맥락 기술 |

**전환 아키텍처**:

```
현재: .claude/agent-memory/
├── skills/strategies.jsonl          # 성공 전략 (append-only)
├── skills/anti-patterns.jsonl       # 실패 패턴 (append-only)
├── scorer-evolution.jsonl           # 스코러 변경 기록
└── refinement/attempts/*.jsonl      # 시도 이력

전환: .claude/agent-memory/
├── raw/                             # Layer 1: Immutable (기존 JSONL 보존)
│   ├── attempts/*.jsonl             # 시도 이력 (변경 없음)
│   └── imports/                     # JSONL → raw로 마이그레이션된 원본
├── wiki/                            # Layer 2: LLM-maintained
│   ├── index.md                     # 전략/안티패턴/스코러 카탈로그
│   ├── log.md                       # 학습 연대기
│   ├── strategies/                  # 전략별 페이지 (교차 참조 포함)
│   ├── anti-patterns/               # 안티패턴별 페이지
│   └── scorer-insights/             # 스코러 진화 인사이트
└── schema.md                        # 위키 운영 규칙
```

**`/refine` 연동 변경**:

| 현재 | 전환 후 |
|------|--------|
| KEEP → `strategies.jsonl`에 1줄 append | KEEP → `wiki/strategies/`에 페이지 생성/업데이트 + index 업데이트 |
| DISCARD → `anti-patterns.jsonl`에 1줄 append | DISCARD → `wiki/anti-patterns/`에 페이지 생성 + 관련 전략에 wikilink |
| 완료 → `scorer-evolution.jsonl`에 1줄 | 완료 → `wiki/scorer-insights/`에 페이지 + lint 실행 |
| 다음 run Audit → JSONL 전체 로드 | 다음 run Audit → `index.md`에서 관련 페이지만 선택적 로드 |

**호환성**: 기존 JSONL 데이터를 `raw/imports/`로 이동 후 초기 위키 페이지로 ingest.
롤백 가능 — JSONL은 삭제하지 않고 raw로 보존.

**Scorer 항목 추가** (ROOT scorer):
```
W4: agent-memory/wiki/index.md 존재
W5: /refine KEEP 시 위키 페이지 생성 확인
W6: /refine 완료 시 lint 실행 확인
```

**위험**: 중간. `/refine` SKILL.md의 KEEP/DISCARD 후처리 로직 변경 필요.
단, 기존 JSONL은 보존되므로 롤백 안전.

---

### Phase 3: Meta-Evolution Observation Wiki

**목표**: ROOT Agent의 관찰 결과를 위키로 축적하여 장기 시스템 지능 확보.

**근거**: 현재 가장 큰 지식 손실 지점. Meta-Evolution 관찰은 `/tmp/agent.log`에만 존재하고
컨테이너 재시작 시 소멸. 동일한 시스템 문제를 반복 진단하는 원인.

**구조**:
```
knowledge/                           # ROOT 전용 (sub-project로 sync 안 됨)
├── raw/
│   ├── observations/                # 관찰 로그 (docker exec 결과 스냅샷)
│   │   ├── 2026-04-07-<sub-project>-run1.md
│   │   └── 2026-04-14-<sub-project>-run2.md
│   ├── reflexions/                  # 시스템 수준 반성
│   └── external/                    # 외부 리서치 (autoresearch 생태계 등)
├── wiki/
│   ├── index.md
│   ├── log.md
│   ├── system-patterns/             # 반복되는 시스템 문제/해결 패턴
│   │   ├── pipefail-in-scorer.md
│   │   └── sync-parity-drift.md
│   ├── evolution-history/           # .claude/ 변경 이력과 효과
│   │   ├── refine-dual-format.md    # "scorer 이중 포맷 → JSON 단순화" 결정
│   │   └── rubrics-addition.md
│   └── sub-project-profiles/        # 프로젝트별 특성 프로파일
│       └── <sub-project>.md
└── schema.md
```

**Meta-Evolution 워크플로우 연동**:

```
현재:                                전환 후:
1. 관찰 (docker exec)               1. 관찰 (docker exec)
2. 진단                             2. 관찰 결과 → raw/observations/ 저장
3. .claude/ 수정                    3. /wiki ingest (관찰 → 위키 업데이트)
4. sync + restart                    4. 진단 (위키 참조 — 유사 과거 사례 검색)
                                     5. .claude/ 수정
                                     6. 수정 결과 → wiki/evolution-history/ 기록
                                     7. sync + restart
```

**핵심 가치**: 관찰 10회 후 위키에 패턴이 축적됨 →
"이 문제는 과거 3번 발생했고, 원인은 X였고, 해결책은 Y였다"를 자동으로 파악 가능.

**Scorer 항목 추가** (ROOT scorer):
```
W7: knowledge/ 디렉토리 존재
W8: knowledge/schema.md 존재
W9: knowledge/wiki/index.md 존재
```

**위험**: 중간. `knowledge/`는 ROOT 전용이므로 sub-project에 영향 없음.
단, CLAUDE.md §6 Meta-Evolution 절차에 위키 단계 추가 필요.

---

## 3. 실행 우선순위 및 일정

```
Phase 1 ─────────────────►  Phase 2 ─────────────────►  Phase 3
/wiki skill 추가              agent-memory 위키 전환      관찰 위키 구축
(독립 기능, 저위험)           (/refine 연동, 중위험)      (Meta-Evolution 연동)

산출물:                       산출물:                      산출물:
- skills/wiki/SKILL.md        - agent-memory/wiki/         - knowledge/
- schema-template.md          - /refine SKILL.md 수정      - CLAUDE.md §6 수정
- ROOT scorer W1-W3           - ROOT scorer W4-W6          - ROOT scorer W7-W9
- README 업데이트             - 마이그레이션 스크립트       - 관찰 자동화 스크립트
```

### Phase 간 의존성

```
Phase 1 → Phase 2: /wiki skill의 ingest/query/lint 메커니즘을
                    agent-memory 위키에 재사용
Phase 2 → Phase 3: agent-memory 위키 구조를
                    knowledge/ 관찰 위키에 확장
```

---

## 4. 차별화 포지셔닝 변화

### 현재 비교표 (landscape.md 기준)

| Feature | autoresearch | Hermes | EvoAgentX | **claude-meta-autoagent** |
|---------|:---:|:---:|:---:|:---:|
| Keep/discard loop | Yes | Yes | Yes | **Yes** |
| Cross-run memory | No | Skills | Partial | **Yes (JSONL)** |
| Meta-evolution | No | No | No | **Yes** |
| Knowledge accumulation | No | No | No | **No** |

### Phase 3 완료 후

| Feature | autoresearch | Hermes | EvoAgentX | **claude-meta-autoagent** |
|---------|:---:|:---:|:---:|:---:|
| Keep/discard loop | Yes | Yes | Yes | **Yes** |
| Cross-run memory | No | Skills | Partial | **Yes (Wiki)** |
| Meta-evolution | No | No | No | **Yes** |
| Knowledge accumulation | No | No | No | **Yes (LLM Wiki)** |

**새로운 차별점**: 코드 진화(autoresearch) + 지식 진화(LLM Wiki) + 시스템 진화(Meta-Evolution)를
하나의 통합 프레임워크에서 제공하는 유일한 시스템.

---

## 5. 위험 요소 및 완화

| 위험 | 심각도 | 완화 |
|------|:------:|------|
| 위키 유지 비용이 JSONL보다 높음 | 중 | Phase 2에서 자동화 (ingest/lint를 /refine에 내장) |
| 위키 페이지 수 폭발 | 중 | Consolidation tier 적용 (v2 패턴) — recent → proven → foundational |
| /refine 루프 속도 저하 (위키 I/O 추가) | 저 | index.md 기반 선택적 로드; 전체 위키 스캔 회피 |
| 기존 JSONL 호환성 깨짐 | 저 | raw/imports/로 보존; 롤백 경로 확보 |
| Sub-project로 불필요한 sync | 저 | knowledge/는 ROOT 전용; sync 대상에서 제외 |

---

## 6. 성공 지표

| Phase | 지표 | 측정 방법 |
|-------|------|----------|
| 1 | `/wiki` skill이 외부 프로젝트에서 작동 | sub-project에서 `/wiki init` + `/wiki ingest` 테스트 |
| 2 | /refine KEEP 시 위키 페이지 자동 생성 | agent-memory/wiki/ 파일 수 증가 확인 |
| 2 | Lint가 모순 전략 감지 | 의도적 모순 삽입 후 lint 감지 테스트 |
| 3 | 관찰 10회 후 패턴 축적 확인 | knowledge/wiki/system-patterns/ 페이지 수 ≥ 3 |
| 3 | 반복 진단 감소 | 동일 문제 진단 횟수 추적 (log.md에서 측정) |

---

## 7. 권장 사항

**Phase 1부터 즉시 시작을 권장합니다.**

이유:
1. **저위험**: 기존 기능에 영향 없이 skill만 추가
2. **즉시 가치**: 프로젝트 README에 "code evolution + knowledge evolution" 포지셔닝 가능
3. **생태계 시의성**: LLM Wiki가 2026-04 현재 최고 관심도 (16M+ 조회, 5K+ stars)
4. **학습 효과**: Phase 1에서 skill 구현 경험이 Phase 2-3의 설계를 개선

Phase 2는 Phase 1 완료 후 `/refine` SKILL.md 수정과 함께 진행.
Phase 3는 실제 Meta-Evolution 실행 시 자연스럽게 도입.

---

## Sources

- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [karpathy-llm-wiki Agent Skill](https://github.com/Astro-Han/karpathy-llm-wiki)
- [LLM Wiki v2](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2)
- [현재 프로젝트 분석](../cross-run-learning.md)
- [리서치: LLM Wiki 심층 분석](llm-wiki.md)
- [리서치: 생태계 비교](landscape.md)
