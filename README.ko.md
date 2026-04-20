# claude-meta-autoagent

> 동일한 추론 과제를 두 하위 에이전트에게 부여하고 **A/B 비교 진화 사이클**을 돌리는 메타 에이전트 시스템입니다. 하나(A)는 고정된 baseline, 다른 하나(B)는 진화 가능한 sub-agent. Meta-Agent(ROOT)가 두 산출물을 판정하고, 자기 거버넌스를 개선하고, 사이클 사이에 B를 개선합니다. Human delegate가 Meta-Agent를 감독하며, 최종 사용자가 GOAL을 제시합니다.

## 4계층 아키텍처

이 저장소는 네 개의 역할 계층으로 구성됩니다. 각 계층은 상위 계층 권한의 엄격한 부분집합만 갖습니다.

```
Level 0  최종 사용자 (Human)
         │  ROOT GOAL 설정, 롤백 승인
         ▼
Level 1  Human delegate
         │  ROOT에 GOAL 전달, ROOT 재시작, 롤백 권한
         ▼
Level 2  ROOT — Meta-Agent  (저장소 최상위 .claude/ + CLAUDE.md)
         │  A와 B 판정, 자기 개선, B 개선; A에는 손대지 않음
         ▼  docker exec via scripts/meta/delegate-sub.sh
┌────────┴────────┐
Level 3a            Level 3b
A Sub-Agent         B Sub-Agent
projects/a/         projects/b/
baseline            evolvable
one-shot            /refine + 교차 실행 학습
사이클 중 frozen     사이클 중 frozen,
                    사이클 사이에 ROOT가 개선
```

### 역할 표 (허용 / 금지)

| 계층 | 역할 | 허용 | 금지 |
|---|---|---|---|
| 0 | 최종 사용자 | ROOT GOAL 설정, 롤백 승인 | — |
| 1 | Human delegate | ROOT에 GOAL 전달, ROOT 재시작, 롤백 | A/B/ROOT 파일 직접 수정 |
| 2 | ROOT (Meta-Agent) | A와 B 판정, 자기 개선, B 개선 | A 파일 수정, A/B에 논문 지식 누출, §6 약화·폐지 |
| 3a | A Sub-Agent | `task/ARGUMENT.md`를 첫 원리로부터 생성 | 자신의 `.claude/` 수정, `WebFetch`, `WebSearch` |
| 3b | B Sub-Agent | `task/ARGUMENT.md`를 `/refine`으로 생성 | 자신의 `.claude/` 수정, `WebFetch`, `WebSearch` |

ROOT는 GOAL만 제공합니다. 하위 에이전트가 METHOD를 자율적으로 선택합니다. delegation 프롬프트에는 슬래시 커맨드·파일 경로·명령형 지시가 포함되어서는 안 됩니다 — 원하는 end-state만 서술하고 실행 설계는 하위 에이전트에 맡깁니다.

## 논문 지식 격리

A/B 사이클은 진화 가능한 아키텍처가 baseline보다 동일한 추론 과제에서 더 잘 사고하는지를 측정합니다. 과제는 어떤 논문에서 파생되지만, **논문은 ROOT만 보유**합니다. A와 B는 첫 원리로부터 논증해야 합니다.

격리는 세 층위에서 강제됩니다:

1. **파일시스템** — 논문 자료는 ROOT workspace 루트의 `docs/research/` 아래에 있습니다. A와 B 컨테이너는 각각 `projects/a/`, `projects/b/`를 `/workspaces`로 bind-mount하므로, ROOT의 논문 디렉터리·`scripts/meta/`·외부 workspace를 볼 수 없습니다.
2. **도구 훅 (A/B 내부 PreToolUse)** —
   - `.claude/hooks/web-block.sh`가 `WebFetch`와 `WebSearch`를 차단.
   - `.claude/hooks/paper-leak-guard.sh`가 제한 식별자를 포함한 도구 페이로드를 거부. 훅 소스는 해당 식별자를 **역순 형태로만** 보관하므로, 훅 자체가 차단 대상 forward-form 문자열을 누출하지 않습니다.
3. **프롬프트 사전 필터 (ROOT 측)** — `scripts/meta/delegate-sub.sh`가 모든 GOAL 텍스트를 제한 식별자 목록과 대조해 하나라도 걸리면 launch를 거부합니다. `scripts/meta/paper-leak-audit.sh`는 각 하위 에이전트의 `task/ARGUMENT.md`에 동일한 스캔을 사후 적용하며, 적중 시 사이클이 무효화됩니다.

## 사이클 실행 순서

모든 사이클은 ROOT 소유이며 동일한 10단계를 따릅니다 (상세는 `CLAUDE.md §6`).

0. **Pre-cycle prep** — 새 경로·식별자를 추가 차단해야 하면 양쪽 하위 프로젝트의 paper-leak-guard 역순 패턴을 강화; `projects/b/.frozen` 존재 확인; commit 후 `git tag cycle-NN-pre HEAD`. 이것이 ROOT가 `projects/a/`를 편집할 수 있는 **유일한** 시점이며, A와 B 양쪽에 대칭적이어야 합니다. A의 `.frozen`은 편집 동안 `Bash`로(워킹 트리만) 제거 후, 수정하고, 다시 비트 단위로 복원 — `.frozen`에 대한 순수 `git diff`는 0이어야 합니다.
1. **Task 준비** — `docs/research/cycle-NN/TASK.md` 작성; 제한 식별자를 언급하지 않습니다. 프롬프트에서 의도적으로 생략한 구조적 힌트를 기록해, 사이클 사이 task-framing drift가 보이도록 합니다.
2. **Launch** — `scripts/meta/delegate-sub.sh a "<GOAL>"`와 `scripts/meta/delegate-sub.sh b "<GOAL>"`를 병렬 실행. 새로 빌드된 하위 컨테이너는 `~/.claude/`가 비어 있으므로, launch 전에 ROOT 컨테이너의 `~/.claude/.credentials.json`을 각 하위 컨테이너로 복사(`chmod 600`)해야 합니다.
3. **Observe** — `docker exec`로 프로세스 생존, `/tmp/agent.log`, git 상태, 산출물 존재, 그리고 B의 `.refinement-active`/attempts JSONL/`.refine-output`을 관측.
4. **Paper-leak audit** — 각 `projects/<a|b>/task/ARGUMENT.md`에 `scripts/meta/paper-leak-audit.sh` 실행. 적중은 실격.
5. **Judge** — 각 ARGUMENT.md를 `docs/research/…/judgment-rubric.md` 기준으로 채점; 해당 사이클의 `JUDGMENT.md`를 criterion 단위로 기록.
6. **Improve ROOT** — 비교에서 드러난 약점을 해결하는 `.claude/` 또는 `CLAUDE.md` 변경을 commit.
7. **Improve B** — B 고유 약점을 해결하는 `projects/b/.claude/` 또는 `projects/b/CLAUDE.md` 변경을 commit(`Bash`로 unfreeze → edit → 비트 단위 refreeze).
8. **A 무변경 확인** — `git diff --quiet cycle-NN-pre -- projects/a/`가 성립해야 함.
9. **Log** — cycle-log에 사이클 요약을 append.
10. **Push** — `git push origin main`.

직접 `docker exec ... claude -p`는 금지됩니다. `.claude/hooks/meta-evolution-guard.sh` 훅이 차단하며, 모든 delegation은 `scripts/meta/delegate-goal.sh` 또는 `scripts/meta/delegate-sub.sh`를 통과해야 합니다.

## 사이클을 처음부터 launch하기

요구사항: Docker (devcontainer 내부에서 실행 시 `docker.sock` 마운트 필요), Claude Code CLI v2.1+, 그리고 ROOT 컨테이너가 이미 인증(`~/.claude/.credentials.json`)되어 있어야 합니다.

```bash
# 1. ROOT 컨테이너 기동
cd .devcontainer && docker compose up -d && cd ..

# 2. A, B 두 하위 컨테이너 기동
cd projects/a/.devcontainer && docker compose up -d && cd ../../..
cd projects/b/.devcontainer && docker compose up -d && cd ../../..

# 3. 각 하위 컨테이너에 Claude 자격증명 주입
for c in claude-meta-autoagent-a claude-meta-autoagent-b; do
  docker cp ~/.claude/.credentials.json "$c":/home/vscode/.claude/.credentials.json
  docker exec "$c" chmod 600 /home/vscode/.claude/.credentials.json
done

# 4. ROOT 컨테이너에서: pre-cycle prep, tag, delegate
#    (GOAL 텍스트는 ROOT 책임이며, 소스 논문을 명시하지 않고
#     추론 end-state를 서술해야 함)
git tag cycle-NN-pre HEAD
scripts/meta/delegate-sub.sh a "<GOAL>" &
scripts/meta/delegate-sub.sh b "<GOAL>" &
wait

# 5. 관측, audit, 판정, 개선, push — CLAUDE.md §6 참조
```

ROOT 컨테이너 내부에서 돌아가는 Claude 세션(= Meta-Agent)이 위 10단계를 수행합니다. 모든 행위는 기록됩니다 — delegation마다 `.claude/.delegate-log/`에 기록되고, 사이클마다 최상위 `cycle-log.md`에 요약이 추가되며, `docs/research/.../cycle-NN/` 아래의 각 JUDGMENT.md는 불변 사이클 산출물입니다.

## 교차 실행 학습 (B 전용)

B는 `/refine`과 `.claude/agent-memory/` 아래의 세 JSONL 메모리 파일을 갖습니다:

| 파일 | 기록 시점 | 이후 실행에서 읽는 곳 |
|---|---|---|
| `skills/strategies.jsonl` | /refine iteration이 KEEP으로 종료 | audit 단계 |
| `skills/anti-patterns.jsonl` | /refine iteration이 DISCARD로 종료 | audit 단계 |
| `scorer-evolution.jsonl` | /refine 실행 완료 | meta 리뷰 |

A는 `/refine`이 없고 agent-memory도 축적하지 않습니다. 이것이 사이클이 측정하는 제어된 비대칭입니다. reflexion / skill-library / scorer-evolution 메커니즘의 상세는 `docs/cross-run-learning.md`를 참조하세요.

## 저장소 레이아웃

```
claude-meta-autoagent/
├── CLAUDE.md                           # ROOT 거버넌스 (§6 Meta-Evolution — A/B 사이클)
├── .claude/                            # ROOT 에이전트 시스템 (hooks, skills, agents, rules)
├── .devcontainer/                      # ROOT 컨테이너
├── docs/
│   └── research/                       # ROOT-전용 논문 자료 및 사이클별 JUDGMENT
├── projects/
│   ├── a/                              # Level-3a baseline (karpathy-skills만)
│   └── b/                              # Level-3b evolvable (ROOT-subset, §6 제외)
├── scripts/
│   └── meta/
│       ├── delegate-goal.sh            # 일반 GOAL-not-METHOD delegation wrapper
│       ├── delegate-sub.sh             # 논문 키워드 사전 필터가 포함된 A/B wrapper
│       ├── paper-leak-audit.sh         # ARGUMENT.md 사후 스캐너
│       ├── completion-checker.sh
│       └── portability-check.sh
├── wip/                                # 다중 세션 task 상태
└── cycle-log.md                        # 사이클별 요약 로그
```

각 하위 프로젝트의 역할과 launch 명령은 `projects/a/README.md`와 `projects/b/README.md`를 참조하세요.

## 요구사항

- Claude Code CLI v2.1+
- Docker (devcontainer 내부에서 실행 시 `docker.sock` 마운트 필요)

GPU 불필요.

## 라이선스

MIT
