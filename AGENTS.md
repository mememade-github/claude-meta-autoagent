# AGENTS.md — MEMEMADE Workspace (Codex CLI)

> **Codex equivalent of CLAUDE.md.** Codex CLI는 본 `AGENTS.md`, `.codex/`, `.agents/skills/`를
> 기준으로 동작합니다. Claude Code(`CLAUDE.md`/`.claude/`)와 동일 거버넌스를 형식 변환한 미러.
>
> **§6 Meta-Evolution은 본 파일에 포함되지 않습니다.** Meta-Evolution은 Claude 측 책임으로 한정.
> Codex는 일반 코딩 작업과 거버넌스만 수행.

## Behavioral Foundation

[`.agents/rules/behavioral-core.md`](.agents/rules/behavioral-core.md) — Karpathy 4-rule
(Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution).
작업 시작 시 `Read` 도구로 우선 로드.

## Identity & Project Structure

- **Workspace**: MEMEMADE_ROOT (`/workspaces/`)
- **Environment**: Dev Container (Ubuntu 22.04, WSL2, user=vscode)

```
/workspaces/                        # MEMEMADE_ROOT (this repo)
├── CLAUDE.md                       # Governance — Claude
├── AGENTS.md                       # Governance — Codex (this file, mirror)
├── PROJECT.md                      # Domain context
├── REFERENCE.md                    # Commands and procedures
├── ARCHITECTURE.md                 # System design
├── .env/                           # Credentials (gitignored)
├── .claude/                        # Claude Code system (ground truth)
├── .agents/                        # Codex agent assets (mirror of .claude/)
├── .codex/                         # Codex CLI config + hooks
├── scripts/
│   └── sync-agents-mirror.sh       # .claude/ → .agents/ 단방향 동기화
└── products/                       # Product repositories (gitignored, independent)
```

## INTEGRITY — every claim verified by execution

**Every claim must be verified by execution before statement.**

- Run tests and show output before claiming "tests pass"
- Execute the build and confirm success before claiming "build succeeds"
- Test functionality and demonstrate results before claiming "works"

## Operational Gates

### Destructive Operations (APPROVAL REQUIRED)

Require explicit user approval before executing:
`rm -rf`, `mv`/`cp` (overwrite), `git push --force`, `git reset --hard`, `DROP`/`DELETE` (DB)

### Pre-Commit Gate (automated by .codex/hooks/pre-commit-gate.sh)

Before ANY `git commit`:
1. Run verification for affected code
2. All checks MUST pass before commit. No `--no-verify`.

## Automated Workflow (MANDATORY)

자동 hook으로 강제. 사용자 명령 불필요.

### Session Start

- Hook이 주입: 현재 branch, 활성 WIP tasks, 환경 정보
- WIP tasks 있으면 즉시 README.md 읽고 작업 재개
- 없으면 readiness 보고 + 사용자 지시 대기
- MEMORY.md의 Known Issues 항상 확인

### Change Evaluation

- **유의미 변경**: `refine` skill (`.agents/skills/refine/`) 사용 — 평가 루프
- **사소 변경** (typo, 단일 config): 직접 수정 OK
- 자가 평가 금지. `evaluator` skill 위임.

### Multi-Session Tasks

- 세션 넘는 task → `wip-manager` skill (`.agents/skills/wip-manager/`)
- WIP 위치: `wip/task-YYYYMMDD-description/README.md`
- 다음 세션 자동 재개 (SessionStart hook)
- 완료 시 WIP 디렉토리 삭제

### Skill Delegation

> Codex CLI는 파일 기반 커스텀 서브에이전트 선언을 아직 공식 지원하지 않으므로,
> 기존 에이전트 책임은 `.agents/skills/` 하위 스킬로 흡수했습니다.

| Skill | Invocation |
|-------|-----------|
| refine | 유의미 변경, 반복 정제 필요 |
| evaluator | 변경 후 (1-pass review); refine loop 내 |
| wip-manager | 세션 넘는 task |
| status | Workspace status |
| verify | Pre-commit verification |

## Coding Rules

1. **Protect secrets** — credentials은 `.env/` (gitignored). 절대 커밋 금지.
2. **Fix root causes** — 인프라/config/배포/코드 전반 진단. 인프라 한계 회피용 코드는 workaround.
3. **Explicit failure** — 모든 작업은 명시적으로 성공 또는 실패. 임의 성공 금지.
4. **Read first** — 수정 전 기존 코드 읽기
5. **Match existing style** — 새 스타일 강요 금지
6. **No speculative features** — 요청 외 기능 추가 금지

## Communication

- **Language**: 사용자에게 응답할 때 항상 한국어.

## Environment

- **Server**: cp001.mememade.com (Docker Swarm, single node)
- **Domain**: mememade.com (HTTPS via Traefik v3)
- **Claude Code**: Native binary (~/.local/bin/claude, auto-updated)
- **Codex CLI**: npm global (~/.npm-global/bin/codex)
- **Persistent volumes**: `~/.claude` (Claude auth), `~/.codex` (Codex auth)

## Behavioral Rules (Codex 미러)

Claude `CLAUDE.md`가 `.claude/rules/`를 참조하는 것과 동등하게, Codex 작업 시
다음 규칙 파일을 우선 적용 (`Read` 도구로 작업 시작 시 로드):

- [.agents/rules/behavioral-core.md](.agents/rules/behavioral-core.md) — Karpathy 4-rule
- [.agents/rules/devcontainer-patterns.md](.agents/rules/devcontainer-patterns.md) — DevContainer DinD 방지

> **운영 원칙**: `.claude/rules/`가 ground truth, `.agents/rules/`는 Codex 호환 미러.
> Claude 측 변경 시 `bash scripts/sync-agents-mirror.sh`로 동기화.

## Extended Reference

도메인 맥락과 명령어는 아래 파일 참조 (Codex AGENTS.md 표준은 `@import` 미지원):

- [PROJECT.md](PROJECT.md) — 인프라, 서비스, 환경
- [REFERENCE.md](REFERENCE.md) — 명령어, 절차
- [ARCHITECTURE.md](ARCHITECTURE.md) — 시스템 설계

---

*Last updated: 2026-04-30 — initial Codex parity (PLAN-2026-033 derived from poc-rag)*
