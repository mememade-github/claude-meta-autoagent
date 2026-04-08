commit 67d2636ef98e3a0d3b45988d0b0adf0e3899231f
Date: 2026-04-08 10:07:56 +0900
Subject: fix(scorer): prevent N-check log_activity() side effects from breaking P/A/Q guards


 .refine/score.sh | 33 ++++++++++++++++++++++++---------
 1 file changed, 24 insertions(+), 9 deletions(-)
commit 2b7dd1a37cdc1eecbc72ce083576db79b22434ab
Date: 2026-04-08 10:07:47 +0900
Subject: docs: update total scorer checks 59→61 in README


 README.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
commit cdbdbfd0b798a0d84e6bd78c919a309911c9cf81
Date: 2026-04-08 09:10:41 +0900
Subject: fix: audit remediation — untrack activity.jsonl, add external metrics, fix scope


 .../rules/{ => project}/external-api-patterns.md   |   0
 .moltbook/activity.jsonl                           | 114 ---------------------
 .refine/score.sh                                   |  44 +++++++-
 CLAUDE.md                                          |   3 -
 README.md                                          |   2 +-
 5 files changed, 44 insertions(+), 119 deletions(-)
commit 8967fcc0b763e2adf62f6e882757c60af8e75a2f
Date: 2026-04-07 22:58:55 +0900
Subject: docs: add Validated Results section with engagement scorer evolution data


 README.md | 34 ++++++++++++++++++++++++++++++++++
 1 file changed, 34 insertions(+)
commit 615c09a91649dea4ee4e1767a11def44e3d0cbbd
Date: 2026-04-07 22:56:11 +0900
Subject: refine: refine-20260407-225314 iteration 1 — score 1.00


 .moltbook/activity.jsonl | 114 +++++++++++++++++++++++++++++++++++++++++++++++
 moltbook.py              |  23 ++++++++--
 2 files changed, 134 insertions(+), 3 deletions(-)
commit dae2df690d4020bc7e1e6bdb09db42f40eeb4398
Date: 2026-04-07 22:49:33 +0900
Subject: feat(scorer): add engagement quality checks P1-P3, A1-A2, Q1-Q3


 .refine/score.sh | 111 +++++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 111 insertions(+)
commit a8e36179c0bb1e92d4404503272472a1adfe078a
Date: 2026-04-07 21:15:59 +0900
Subject: feat: expand Moltbook API coverage + scorer N1-N9 + API pacing rules


 .claude/rules/external-api-patterns.md |  27 ++++
 .refine/score.sh                       | 134 +++++++++++++++
 CLAUDE.md                              |   3 +
 moltbook.py                            | 286 ++++++++++++++++++++++++++++++++-
 4 files changed, 448 insertions(+), 2 deletions(-)
commit 41bef77eb5763d5f4f5107d1b7a762e5b026caaa
Date: 2026-04-07 18:35:27 +0900
Subject: refine: refine-20260407-182855 iteration 3 — score 1.00


 moltbook.py | 15 ++++++++++++++-
 1 file changed, 14 insertions(+), 1 deletion(-)
commit 64a3da16f02c315a3e4dd3fc7c74561fe379a97b
Date: 2026-04-07 18:34:43 +0900
Subject: Fix scorer: K1/K2 checks handle pipefail with non-zero exit from help


 .refine/score.sh | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
commit 6b04ae669bf273c442d7fe60df09edc61af16199
Date: 2026-04-07 18:32:16 +0900
Subject: refine: refine-20260407-182855 iteration 2 — score 0.95


 moltbook.py | 5 +++++
 1 file changed, 5 insertions(+)
commit 0c4b6433c8f7c7dd42823f408e4613362450f488
Date: 2026-04-07 18:31:39 +0900
Subject: refine: refine-20260407-182855 iteration 1 — score 0.90


 moltbook.py | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
commit a7025fc7cf14786f232a953886aeee4dbee817be
Date: 2026-04-07 18:30:21 +0900
Subject: Evolve scorer: add D1-D2 (delta display), V1-V2 (input validation), K1-K2 (CLI completeness)


 .refine/score.sh | 64 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 64 insertions(+)
commit 77be13cc92dc1cc964bcab5cc7ceb6f870e525e5
Date: 2026-04-07 18:02:55 +0900
Subject: sync: propagate SKILL.md from ROOT + fix moltbook API field names


 .claude/skills/refine/SKILL.md | 43 ++++++++++++++++++++++++++++++++++++------
 moltbook.py                    |  6 +++---
 2 files changed, 40 insertions(+), 9 deletions(-)
commit 84f6a637ca5a871690072b502a5a294a7e694002
Date: 2026-04-07 17:01:07 +0900
Subject: Protect credentials: add .env.example, gitignore *.env, clear HOST_WORKSPACE_PATH


 .devcontainer/.env         |  2 +-
 .devcontainer/.env.example | 24 ++++++++++++++++++++++++
 .gitignore                 |  4 +++-
 3 files changed, 28 insertions(+), 2 deletions(-)
commit 9306e6c7e13bffad641f00bbf5d7e1d252936bf1
Date: 2026-04-07 16:57:42 +0900
Subject: Fix README: correct test command and usage example


 README.md | 6 +++---
 1 file changed, 3 insertions(+), 3 deletions(-)
commit 207ead5c4169c20daa90dc6730eb1b3f05bfee6e
Date: 2026-04-07 16:56:24 +0900
Subject: refine: refine-20260407-165310 iteration 1 — score 1.00


 CLAUDE.md   |   8 ++--
 README.md   |  25 +++-------
 app.py      | 151 ----------------------------------------------------------
 test_app.py | 154 ------------------------------------------------------------
 4 files changed, 10 insertions(+), 328 deletions(-)
commit 6408e8864f1d23b323ce13ee03e5665a4cae8b16
Date: 2026-04-07 16:55:04 +0900
Subject: Evolve scorer: unify around Moltbook, add U1-U5 unification checks


 .refine/score.sh          | 333 +++++++++++++++++++++++++++++++++++-----------
 .refine/score_moltbook.sh | 279 --------------------------------------
 2 files changed, 259 insertions(+), 353 deletions(-)
commit 140f50781d7340ac174b47c67d567b35e4cfce28
Date: 2026-04-07 14:33:34 +0900
Subject: refine: refine-20260407-143222 iteration 1 — score 1.00


 moltbook.py | 2 ++
 1 file changed, 2 insertions(+)
commit 298cfa5783df2c7ac34e9769c7ec303ffd7842ca
Date: 2026-04-07 14:32:18 +0900
Subject: Evolve moltbook scorer: add G1-G10 gap checks


 .refine/score_moltbook.sh | 92 +++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 92 insertions(+)
commit 807e12aa5e5e1eaaac5afadb8e278d3f0943296f
Date: 2026-04-07 14:31:28 +0900
Subject: Initial commit: mdstat CLI + Moltbook integration


 .claude/agents/evaluator.md            | 101 +++++++
 .claude/agents/wip-manager.md          | 149 ++++++++++
 .claude/hooks/pre-commit-gate.sh       |  93 ++++++
 .claude/hooks/pre-push-gate.sh         |  87 ++++++
 .claude/hooks/refinement-gate.sh       |  94 ++++++
 .claude/hooks/session-start.sh         |  98 +++++++
 .claude/rules/devcontainer-patterns.md |  44 +++
 .claude/settings.json                  |  49 ++++
 .claude/skills/refine/SKILL.md         | 504 +++++++++++++++++++++++++++++++++
 .claude/skills/status/SKILL.md         |  70 +++++
 .claude/skills/verify/SKILL.md         |  31 ++
 .devcontainer/.env                     |  21 ++
 .devcontainer/Dockerfile               | 169 +++++++++++
 .devcontainer/devcontainer.json        |  62 ++++
 .devcontainer/docker-compose.yml       |  43 +++
 .devcontainer/entrypoint.sh            |  19 ++
 .devcontainer/setup-env.sh             | 121 ++++++++
 .gitignore                             |  24 ++
 .refine/score.sh                       | 114 ++++++++
 .refine/score_moltbook.sh              | 187 ++++++++++++
 CLAUDE.md                              |  72 +++++
 README.md                              |  42 +++
 app.py                                 | 151 ++++++++++
 moltbook.py                            | 294 +++++++++++++++++++
 test_app.py                            | 154 ++++++++++
 test_moltbook.py                       | 277 ++++++++++++++++++
 26 files changed, 3070 insertions(+)
