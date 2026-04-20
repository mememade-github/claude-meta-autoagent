# claude-meta-autoagent

> [karpathy/autoresearch](https://github.com/karpathy/autoresearch)에서 영감을 받았습니다 — AI 에이전트가 자율적으로 실험하고, 성공하면 유지하고, 실패하면 폐기하고, 무한히 반복합니다. 동일한 "자율 반복 + keep/discard" 패턴을 **모든 소프트웨어 프로젝트**에 적용하고, **교차 실행 학습**과 **2계층 자기진화 아키텍처**로 확장합니다.

## autoresearch와의 차이점

| | [autoresearch](https://github.com/karpathy/autoresearch) | claude-meta-autoagent |
|---|---|---|
| **루프** | train.py 수정 → 5분 GPU 실행 → val_bpb → keep/discard | 코드 수정 → scorer 실행 → 점수 비교 → keep/discard |
| **범위** | LLM 학습 전용 (GPU 필요) | 모든 소프트웨어 프로젝트 (GPU 불필요) |
| **지시** | program.md (단일 파일) | CLAUDE.md + SKILL.md + hooks (전체 거버넌스 시스템) |
| **학습** | 매 실험 zero-memory | 3-loop 교차 실행 학습 |
| **아키텍처** | 단일 에이전트, 단일 컨테이너 | **2계층**: ROOT는 에이전트 시스템을 진화(메타), Sub-project 에이전트는 코드를 진화(구현) |
| **메트릭** | val_bpb (고정) | 프로젝트별 scorer (사용자 정의) |

**핵심 개선사항:**
1. **교차 실행 메모리** — 성공 전략과 실패 안티패턴을 실행 간 축적 ([상세](docs/cross-run-learning.md))
2. **Scorer 진화** — scorer가 프로젝트와 함께 성장하는지, 정체되었는지 추적
3. **2계층 메타 진화** — ROOT 에이전트가 독립 컨테이너의 sub-project 에이전트를 관측하고 시스템 자체를 개선 ([상세](docs/meta-evolution.md))
4. **범용성** — 웹 앱, API, CLI 도구, 라이브러리 — 테스트 가능한 scorer만 있으면 적용 가능

## 빠른 시작

두 가지 수준 — 필요에 맞는 것을 선택하세요. 전체 가이드: [docs/quickstart.md](docs/quickstart.md)

### Level 1: 외부 프로젝트에 /refine 추가 (가장 간단, 메타 진화 없음)

> 참고: 이것은 standalone /refine만 사용합니다. 2계층 ROOT→Sub-project 전체 시스템은 Level 2를 참조하세요.

```bash
git clone https://github.com/mememade-github/claude-meta-autoagent.git
cp -r claude-meta-autoagent/.claude/ /path/to/your/project/.claude/
```

프로젝트에 `.refine/score.sh`를 만들고: `/refine "improve production quality"`

### Level 2: 2계층 메타 진화 전체 구동

```bash
# 모든 명령은 호스트(또는 docker.sock이 마운트된 외부 컨테이너)에서 실행

# 1. ROOT 컨테이너 시작
cd claude-meta-autoagent/.devcontainer && docker compose up -d && cd ..

# 2. Sub-project 컨테이너 시작 (독립, projects/<sub-project>/ 아래)
cd projects/<sub-project>/.devcontainer && docker compose up -d && cd ../../..

# 3. Sub-project에 headless 에이전트 실행 (ROOT에서)
docker exec -d <sub-project> bash -c \
  'cd /workspaces && claude --dangerously-skip-permissions \
   -p "Run /refine to improve production quality" \
   > /tmp/agent.log 2>&1'

# 4. ROOT에서 관측
docker exec <sub-project> cat /tmp/agent.log
docker exec <sub-project> git -C /workspaces log --oneline -5
docker exec <sub-project> cat /workspaces/.refine-output

# 5. 시스템 이슈 발견 시 .claude/ 수정, 동기화, 에이전트 재시작
./scripts/sync/sync-claude.sh projects/<sub-project>
```

## 작동 원리

### 아키텍처

ROOT와 Sub-project는 **하나의 통합 시스템**입니다 — Sub-project는 ROOT 저장소 내부(`projects/*/`)에 존재하며 ROOT의 거버넌스 하에 운영됩니다.

```
┌──────────────────── claude-meta-autoagent (단일 시스템) ──────────────────┐
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │  계층 1: ROOT — 메타 진화                                           │  │
│  │  진화 대상: .claude/ 시스템 (hooks, skills, agents, rules)          │  │
│  │                                                                    │  │
│  │  .claude/ (ORIGIN)     사용자가 여기서 운영                         │  │
│  │  ├── skills/refine/    ── /refine 루프                             │  │
│  │  ├── hooks/            ── 게이트                                   │  │
│  │  ├── agents/           ── 평가자                                   │  │
│  │  └── rules/            ── 표준 규칙                                │  │
│  │                                                                    │  │
│  │  Sub-project 관측 ◄── docker exec ────┐                           │  │
│  │  시스템 이슈 진단                      │                           │  │
│  │  .claude/ 수정, 동기화 ───────────────┐│                           │  │
│  └───────────────────────────────────────┼┼──────────────────────────┘  │
│                                           ││                             │
│                     .claude/ 동기화 ──────┘│                             │
│                                            │                             │
│  ┌─────────────────────────────────────────┼─────────────────────────┐  │
│  │  계층 2: Sub-project (projects/*/)      │                        │  │
│  │  진화 대상: 프로젝트 코드와 scorer       │                        │  │
│  │                                         │                        │  │
│  │  .claude/ (ROOT에서 동기화)              │                        │  │
│  │  .refine/score.sh (프로젝트 scorer)      ◄───────────────────────┘  │
│  │  [프로젝트 코드] ── 에이전트가 개선                                │  │
│  │                                                                    │  │
│  │  Headless 에이전트가 /refine 자율 실행                             │  │
│  │  생성물: 커밋, 점수, strategies.jsonl                              │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

### /refine 루프

```
1. DISCOVER   — scorer 읽기, gap 발견
2. BASELINE   — scorer 실행, 기준 점수
3. AUDIT      — gap 분석 + 이력 참조 (전략, 안티패턴)
4. MODIFY     — 최우선 gap 수정 (fresh subagent)
5. EVALUATE   — scorer 재실행
6. KEEP/DISCARD — 기준 점수와 비교
7. RECORD+LEARN — 실패 시 반성, 전략 축적
8. REPEAT     — threshold 또는 최대 반복까지
```

### 교차 실행 학습

| 루프 | 트리거 | 학습 내용 | 저장소 |
|------|--------|----------|--------|
| **Reflexion** | DISCARD | "왜 실패했는가" + 방지 원칙 | attempts JSONL |
| **Skill Library** | KEEP/DISCARD | 성공 전략 / 실패 안티패턴 | strategies.jsonl, anti-patterns.jsonl |
| **Scorer Evolution** | 실행 완료 | scorer 커버리지 gap, 회귀 횟수 | scorer-evolution.jsonl |

[교차 실행 학습 상세 →](docs/cross-run-learning.md)

### 메타 진화: 자기 개선하는 에이전트 시스템

ROOT 에이전트가 sub-project 에이전트를 관측하고 `.claude/` 시스템을 개선합니다:

1. **실행** — sub-project 컨테이너에 headless 에이전트 기동
2. **관측** — `docker exec`로 프로세스, 로그, git, 점수, 파일 변경 확인
3. **진단** — 프로젝트 코드 문제인가, 에이전트 시스템 문제인가?
4. **수정** — ROOT의 `.claude/` portable 파일 개선
5. **동기화** — sub-project에 반영, 에이전트 재시작, 재관측

[메타 진화 상세 →](docs/meta-evolution.md)

## 프로젝트 구조

```
claude-meta-autoagent/                    # ROOT — 단일 통합 시스템
├── .claude/                              # 에이전트 시스템 ORIGIN (Sub-project에 동기화)
│   ├── agents/evaluator.md, wip-manager.md
│   ├── hooks/pre-commit-gate, session-start, refinement-gate, pre-push-gate
│   ├── skills/refine, status, verify
│   └── rules/devcontainer-patterns.md
│
├── .devcontainer/                        # ROOT 컨테이너
│   ├── Dockerfile, docker-compose.yml    # Claude Code + MCP + 도구
│   ├── entrypoint.sh, setup-env.sh       # 자동 설정
│   └── .env                              # 컨테이너 ID + 포트
│
├── scripts/
│   ├── sync/sync-claude.sh               # ROOT → Sub-project 동기화
│   └── meta/completion-checker.sh        # 커밋 전 검증
│
├── projects/                             # Sub-project들 (ROOT 시스템의 일부)
│   └── <sub-project>/                    # 계층 2 Sub-project
│       ├── .claude/                      # ROOT에서 동기화 (읽기 전용 거버넌스)
│       ├── .devcontainer/                # 격리 컨테이너 (ROOT가 관측)
│       ├── .refine/score.sh              # 프로젝트 고유 scorer
│       ├── CLAUDE.md                     # 프로젝트 거버넌스 (§6 메타 진화 없음)
│       └── <프로젝트 소스 + 테스트>        # 애플리케이션 코드
│
├── docs/                                 # 문서
│   ├── quickstart.md, cross-run-learning.md, meta-evolution.md
│
├── CLAUDE.md                             # ROOT 거버넌스 (메타 진화 §6)
└── README.md
```

> Sub-project는 ROOT 시스템의 일부입니다. `.claude/`를 동기화로 받고, 격리 컨테이너에서 실행되며, ROOT가 메타 진화를 위해 관측합니다.

## 좋은 scorer 작성법

Scorer는 이 시스템에서 가장 중요한 파일입니다. 프로젝트의 "품질"이 무엇인지 정의합니다.

1. **사용자가 경험하는 것을 테스트** — 코드 위생이 아닌 실제 기능
2. **모든 상호작용 계층 커버** — API, UI/CLI, 장애 복구
3. **ID 사용** — 각 체크에 F1, E1, C1... 부여, 에이전트가 특정 gap을 타겟
4. **출력 형식** — `SCORE: 0.XX`와 `GAPS: [ID1, ID2, ...]` 출력 필수
5. **Scorer 독립성** — scorer와 프로덕트 코드를 같은 `/refine` iteration에서 동시 수정 금지

## 요구사항

- [Claude Code](https://claude.ai/download) CLI (v2.1+)
- Docker (DevContainer 및 메타 진화용)
- 테스트 가능한 기능이 있는 프로젝트

GPU 불필요.

## 실증 결과

이 시스템은 실제 headless 에이전트로 end-to-end 검증되었습니다:
- Sub-project 에이전트: /refine으로 scorer가 있는 sub-project를 여러 /refine iteration에 걸쳐 자율 개선
- ROOT 에이전트: sub-project를 관측하고, scorer 버그와 코드 gap을 정확히 분류, scorer 독립성 준수
- 교차 실행 학습: strategies.jsonl이 iteration 간 축적, DISCARD 시 anti-patterns 기록
- 2컨테이너 배포 검증 완료 (ROOT + sub-project, 독립 포트, `.claude/` 동기화 공유)

## 라이선스

MIT
