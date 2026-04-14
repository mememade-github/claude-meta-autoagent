# LLM Wiki Pattern: Deep Research (2026)

> Karpathy의 LLM Wiki 패턴 심층 분석 — 아키텍처, 구현, RAG 비교, 확장.
> Sources: [Karpathy gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f),
> [karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki),
> [LLM Wiki v2](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2)

---

## Origin

2026년 4월, Andrej Karpathy가 X에 게시: LLM을 코드 생성이 아닌 **개인 지식 베이스 구축**에
사용하는 워크플로우. 16M+ 조회수, GitHub Gist 5,000+ stars.

핵심 통찰: "지식 베이스 유지의 지루한 부분은 읽기나 사고가 아니라 **정리(bookkeeping)**다.
LLM은 정리를 포기하지 않는다. 인간은 포기한다."

---

## Three-Layer Architecture

```
┌─────────────────────────────────────────────┐
│  Layer 3: Schema (CLAUDE.md)                │
│  — 구조, 명명 규칙, 워크플로우 정의          │
├─────────────────────────────────────────────┤
│  Layer 2: Wiki (wiki/)                       │
│  — LLM이 생성·유지하는 마크다운 페이지       │
│  — index.md (카탈로그) + log.md (연대기)     │
│  — concepts/ entities/ sources/ comparisons/ │
├─────────────────────────────────────────────┤
│  Layer 1: Raw Sources (raw/)                 │
│  — 불변(immutable) 원본 문서                 │
│  — articles/ papers/ repos/ data/ images/    │
└─────────────────────────────────────────────┘
```

**원칙**: Raw는 LLM이 읽기만 함. Wiki는 LLM이 전적으로 소유. Schema가 행동을 규정.

---

## Directory Structure

```
my-research/
├── raw/                    # Layer 1: Immutable sources
│   ├── articles/
│   ├── papers/
│   ├── repos/
│   ├── data/
│   └── images/
├── wiki/                   # Layer 2: LLM-maintained
│   ├── index.md            # Master catalog (every page, one-line summary)
│   ├── log.md              # Append-only: ## [YYYY-MM-DD] ingest | Title
│   ├── overview.md
│   ├── concepts/           # Domain concepts (attention-mechanism.md)
│   ├── entities/           # Organizations/people (openai.md)
│   ├── sources/            # Individual source summaries
│   └── comparisons/        # Comparative analysis pages
├── outputs/                # Generated reports, lint results
├── CLAUDE.md               # Layer 3: Schema
└── .gitignore
```

---

## Three Core Operations

### 1. Ingest

새 소스 문서를 처리하여 위키에 통합:

1. `raw/`의 문서 읽기 + 핵심 takeaway 추출
2. `wiki/sources/`에 요약 페이지 생성
3. 관련 10-15개 위키 페이지에 걸쳐 cascade 업데이트
4. 필요 시 새 concept/entity 페이지 생성
5. `index.md` 업데이트
6. `log.md`에 작업 기록 추가

**단일 ingest가 수십 개 페이지를 터치** — 지식이 그래프 전체에 전파됨.

### 2. Query

위키를 검색하여 답변 합성:

1. `index.md`로 관련 페이지 식별
2. 대상 페이지 로드 + 답변 합성
3. `[[wikilink]]`로 소스 인용
4. 가치 있는 답변은 새 위키 페이지로 영구 보존

**시간이 지날수록 쿼리 품질이 향상** — 각 ingest가 미래 쿼리를 개선.

### 3. Lint

주기적 건강 검사:

- **모순(Contradictions)**: 페이지 간 상충하는 주장
- **고아 페이지(Orphans)**: 들어오는 링크 없는 페이지
- **누락 개념(Missing concepts)**: 참조되지만 페이지가 없는 토픽
- **오래된 주장(Stale claims)**: 새 소스로 대체된 어설션
- **조사 공백(Investigation gaps)**: 추가 연구 필요 영역

결과: `outputs/lint-YYYY-MM-DD.md`에 저장

---

## Page Frontmatter

모든 위키 페이지에 필수:

```yaml
---
title: Page Title
type: concept | entity | source-summary | comparison
sources:
  - raw/papers/filename.md
related:
  - "[[related-concept]]"
created: 2026-04-14
updated: 2026-04-14
confidence: high | medium | low
---
```

---

## LLM Wiki vs RAG

| 차원 | RAG | LLM Wiki |
|------|-----|----------|
| **상태** | Stateless — 매 쿼리 독립 | Stateful — 지식 축적 |
| **인프라** | Vector DB + 임베딩 파이프라인 | 마크다운 파일만 |
| **교차 참조** | 쿼리마다 ad-hoc 발견 | LLM이 사전 구축, 항상 가용 |
| **유지보수** | 임베딩 업데이트, 인덱스 리빌드 | LLM이 ingest 시 페이지 업데이트 |
| **쿼리당 토큰** | 높음 (검색 + 재순위 + 생성) | 낮음 (인덱스 + 대상 페이지 읽기) |
| **추적성** | 청크 수준 인용 (손실) | 소스 수준 → `raw/` 직접 링크 |
| **모순 감지** | 미감지 — 상충 청크 공존 | Lint에서 플래그 |
| **적정 규모** | 대규모 (수만~수백만 문서) | 개인/팀 (수백~수천 페이지) |
| **토큰 절감** | — | 최대 95% (naive loading 대비) |

### 선택 기준

**LLM Wiki 적합**:
- 100-200개 이하 소스 문서
- 지식 축적이 중요 (각 소스가 미래 쿼리 개선)
- 높은 추적성 (모든 주장 → 원본 소스 링크)
- 제로 인프라 선호
- 일관성 검사 > 속도

**RAG 적합**:
- 수만~수백만 문서
- 빈번한 문서 변경 (전체 re-ingest 비현실적)
- 밀리초 수준 쿼리 지연 필요
- 접근 권한이 다른 팀 간 공유

**하이브리드**: 안정 지식은 Wiki in context, 롱테일 검색은 RAG — 최적 조합.

---

## Tool Stack

### Minimum Viable

| 도구 | 역할 | 필수 |
|------|------|:---:|
| LLM Agent (Claude Code 등) | 위키 유지 엔진 | Yes |
| 폴더 (raw/ + wiki/ + CLAUDE.md) | 저장소 | Yes |
| Git | 버전 관리 | 권장 |

### Full Stack

| 도구 | 역할 |
|------|------|
| [Obsidian](https://obsidian.md/) | 위키 프론트엔드 (Graph View, Backlinks) |
| [QMD](https://github.com/Tobi-De/qmd) | 시맨틱 검색 (BM25 + vector + LLM re-ranking) |
| Obsidian Web Clipper | 웹 문서 → 마크다운 변환 |
| Dataview plugin | 프론트매터 기반 구조화 쿼리 |
| Marp | 위키 → 프레젠테이션 변환 |

### Agent Skill 구현

**[karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki)** (Astro-Han):
- Agent Skills 호환 — Claude Code, Cursor, Codex CLI, OpenCode
- 설치: `npx add-skill Astro-Han/karpathy-llm-wiki`
- 실적: 94 위키 문서, 99 소스, 87 로그 엔트리 (7일)

---

## LLM Wiki v2 (확장)

[rohitg00/LLM Wiki v2](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2)에서
agentmemory 구축 경험을 기반으로 v1을 확장.

### 핵심 추가 기능

#### Memory Lifecycle

v1은 모든 콘텐츠를 동등하게 영구 보존. v2는:

- **Confidence scoring**: 소스 수, 최신성, 모순 기반 신뢰도 메타데이터
- **Supersession**: 새 정보가 구 주장을 명시적으로 교체 (공존 불가)
- **Forgetting curves**: Ebbinghaus 스타일 감쇠 — 접근/새 소스로 강화되지 않으면 우선순위 하강
  - 아키텍처 결정: 느리게 감쇠
  - 일시적 버그: 빠르게 감쇠

#### Consolidation Tiers (4계층 모델)

```
Working Memory   — 최근 관찰, 미처리
       ↓
Episodic Memory  — 압축된 세션 요약
       ↓
Semantic Memory  — 교차 세션 사실
       ↓
Procedural Memory — 워크플로우, 패턴
```

#### Knowledge Graph Structure

- **Entity extraction**: 타입화된 엔티티 자동 추출 (사람, 프로젝트, 라이브러리, 개념, 파일, 결정)
- **Typed relationships**: `uses`, `depends_on`, `contradicts`, `caused`, `fixed`, `supersedes`
- **Graph traversal**: "Redis 업그레이드 시 영향 범위?"같은 쿼리 → 의존성 엣지 순회

#### Automation (Event-Driven Hooks)

| 이벤트 | 동작 |
|--------|------|
| 새 소스 추가 | Auto-ingest + entity extraction + graph update + index refresh |
| 세션 시작 | 최근 활동 기반 컨텍스트 로딩 |
| 세션 종료 | 관찰/인사이트로 압축 |
| 메모리 쓰기 | 모순 감지 → supersession 트리거 |
| 스케줄 | 주기적 lint, consolidation, retention decay |

#### Self-Healing Lint

v1: 문제 보고만. v2: **자동 수리** — 고아 페이지, 오래된 주장, 깨진 참조를 직접 해결.

#### Scale (100+ 페이지)

- Hybrid retrieval: BM25 + vector search + graph traversal
- Reciprocal rank fusion으로 3개 스트림 병합
- `index.md`는 ~100 페이지 이후 보조 역할로 전환

---

## Metaphor: Wiki as Compiled Output

```
raw/      → Source Code (불변)
LLM       → Compiler
wiki/     → Compiled Output (생성물)
lint      → Tests
query     → Runtime Execution
```

위키를 문서가 아닌 **컴파일된 산출물**로 취급. 추적 가능하고, 유지보수 가능하며,
Graph RAG 없이도 구조화된 지식 관리가 가능.

---

## Community Implementations

| 프로젝트 | 유형 | 설명 |
|----------|------|------|
| [karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki) | Agent Skill | Claude Code/Cursor/Codex 호환 |
| [llm_wiki](https://github.com/nashsu/llm_wiki) | Desktop App | 크로스플랫폼 데스크탑 앱 |
| [LLM Wiki v2](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2) | Extended Pattern | Memory lifecycle + knowledge graph |
| claude-obsidian | Skill | Obsidian vault에 autoresearch 연구 통합 |
| CacheZero | npm Package | 단일 npm install 구현 |
| llm-wiki-compiler | Tool | 마크다운 → 토픽 기반 위키 컴파일 |

---

## Relation to claude-meta-autoagent

LLM Wiki와 autoresearch/refine은 **상호 보완적** 패턴:

| 측면 | LLM Wiki | autoresearch / /refine |
|------|----------|----------------------|
| 대상 | 지식 (Knowledge) | 코드 (Code) |
| 축적물 | 위키 페이지 | 성공 전략 + 안티패턴 |
| 평가 | Lint (일관성) | Scorer (점수) |
| 진화 | 스키마 공진화 | Scorer evolution |

**잠재적 통합 포인트**:
- `/refine` 결과를 LLM Wiki로 축적 (실험 기록 → 지식 페이지)
- Scorer evolution 이력을 위키 sources로 ingest
- 관찰 로그를 체계적 위키 엔트리로 정리

---

## Sources

- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki)
- [LLM Wiki v2 gist](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2)
- [Complete Implementation Guide](https://blog.starmorph.com/blog/karpathy-llm-wiki-knowledge-base-guide)
- [LLM Wiki in Production](https://aaronfulkerson.com/2026/04/12/karpathys-pattern-for-an-llm-wiki-in-production/)
- [LLM Wiki vs RAG](https://www.mindstudio.ai/blog/llm-wiki-vs-rag-markdown-knowledge-base-comparison)
- [VentureBeat — Karpathy LLM Knowledge Base](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an)
- [Analytics Vidhya — LLM Wiki Revolution](https://www.analyticsvidhya.com/blog/2026/04/llm-wiki-by-andrej-karpathy/)
- [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki)
