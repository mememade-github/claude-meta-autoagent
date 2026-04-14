# Autoresearch Ecosystem (194+ Projects)

> Comprehensive catalog of Karpathy autoresearch derivatives and implementations.
> Source: [awesome-autoresearch](https://github.com/yibie/awesome-autoresearch)

## Origin

**[karpathy/autoresearch](https://github.com/karpathy/autoresearch)** (2026-03-07)

Released by Andrej Karpathy, the original autoresearch provides a minimal "agent loop"
for autonomous LLM experimentation:

```
modify train.py → train 5min on H100 → measure val_bpb → keep or revert → repeat
```

Key results:
- 700 experiments in 2 days, 20 optimizations discovered
- val_bpb improvement: 0.9979 → 0.9697 (126 experiments)
- Applying 20 tweaks to larger model: 11% training speedup
- 21,000+ GitHub stars, 8.6M views on announcement

Karpathy's vision: "The goal is not to emulate a single PhD student, it's to emulate
a research community of them." — swarms of agents collaborating asynchronously.

---

## By Domain

### Scientific Research (25 projects)

| Project | Domain | Key Result |
|---------|--------|------------|
| [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) | Idea → Paper pipeline | Multi-stage with self-healing experiments |
| [Sibyl Research System](https://github.com/Sibyl-Research-Team/AutoResearch-SibylSystem) | Autonomous AI scientist | Inner research-iteration + self-evolution |
| [autoresearch-rl](https://github.com/vivekvkashyap/autoresearch-rl) | RL post-training | Iterating training configs with eval improvements |
| [autoresearch-robotics](https://github.com/jellyheadandrew/autoresearch-robotics) | MuJoCo/Gymnasium | Simulator renderings for policy selection |
| [Bio-Autoresearch](https://github.com/monk1337/Bio-Autoresearch) | Drug repurposing | AUPRC 0.284 → 0.761 on PrimeKG |
| [autoresearch-medimage](https://github.com/mattlungrenmd/autoresearch-medimage) | Medical imaging | ChestXray14 2D tasks |
| [autoresearch-cifar10](https://github.com/GuillaumeErhard/autoresearch-cifar10) | Image classification | ResNet under fixed time budgets |
| [MLP-AutoResearch](https://github.com/HuangShengZeBlueSky/MLP_AutoResearch) | MLP classifier | Accuracy 0.9809 → 0.9836 |
| [autoresearch-quantum](https://github.com/saymrwulf/autoresearch-quantum) | Quantum computing | Encoded magic-state experiments |
| [kaggle-autoresearch](https://github.com/aplassard/kaggle-autoresearch) | Kaggle competitions | Titanic, House Prices |
| [autocircuit](https://github.com/qelloman/autocircuit) | Circuit design | SKY130 op-amp with ngspice simulation |
| [fe-autoresearch](https://github.com/ezemriv/fe-autoresearch) | Feature engineering | LightGBM on UCI Bank Marketing |

### Software / Systems Optimization (35 projects)

| Project | Target | Key Result |
|---------|--------|------------|
| [AutoKernel](https://github.com/RightNow-AI/autokernel) | GPU kernels | Karpathy-style on kernel bottlenecks |
| [Flash-MoE](https://github.com/gorroai/flash-moe) | Metal optimization | Qwen3.5-397B on Apple Silicon |
| [WinMoE](https://github.com/idan82labs/WinMoE) | Inference throughput | 0.44 → 1.9 tok/s on Qwen3.5-397B |
| Shopify Liquid | Template engine | Parse+render 53% improvement |
| HashSmith | JVM hash table | 13-32% faster SwissTable |
| 588x SQLite | ETL ingestion | 397s → 0.675s financial data |
| PolyTrader | Signal detection | Latency 25.7ms → 0.46ms |
| Pytest speedups | Test suite | 295s → 71s |
| browser-use | Browser agent | 97% on Online-Mind2Web benchmark |
| Gumroad flaky tests | Test reliability | 206 commits, 13 flaky tests fixed |
| [autoresearch-sudoku](https://github.com/Rkcr7/autoresearch-sudoku) | Rust solver | 312 experiments rewriting solver |

### Finance / Trading (15 projects)

| Project | Market | Approach |
|---------|--------|----------|
| [atlas-gic](https://github.com/chrisworsey55/atlas-gic) | General markets | Keep when Sharpe improves |
| [autoresearch-trading](https://github.com/erix/autoresearch-trading) | SPY strategy | Backtest metric loop |
| [BTCautoresearch](https://github.com/CBaquero/BTCautoresearch) | Bitcoin | Walk-forward forecasting |
| [autoresearch-skfolio](https://github.com/CarloNicolini/autoresearch-skfolio) | Portfolio | Sharpe optimization |
| AutoResearch DEX | Base DEX | Composite 0.421 → 8.176 |
| Paradigm PM Challenge | Prediction markets | 1,039 variants, 2,000+ evals |
| NEPSE quant terminal | Nepal stock exchange | 300+ autoresearch cycles |

### Evaluation / Red Teaming (11 projects)

| Project | Target | Approach |
|---------|--------|----------|
| [Claudini](https://github.com/romovpa/claudini) | LLM attacks | Autoresearch-style adversarial loop |
| [AutoPrompter](https://github.com/gauravvij/AutoPrompter) | Prompt optimization | promptfoo + closed-loop |
| [Autoreason](https://github.com/NousResearch/autoreason) | Subjective tasks | Blind multi-judge Borda scoring |
| [AutoMemory](https://github.com/Shelter41/automemory) | Memory systems | LongMemEval with immutable evaluator |
| Cerebras anti-cheat | Loop integrity | 71 experiments on cheating prevention |
| Autoresearch for agents | Agent accuracy | System prompt optimization 0.05 → 0.80 |

### Infrastructure / Skills / Forks (48 projects)

Key generalization projects:

| Project | Contribution |
|---------|-------------|
| [pi-autoresearch](https://github.com/davebcn87/pi-autoresearch) | Generalized loop + live dashboard + slash-commands |
| [n-autoresearch](https://github.com/iii-hq/n-autoresearch) | Multi-GPU parallelism + adaptive search |
| [CORAL](https://github.com/Human-Agent-Society/CORAL) | Multi-agent with branch-isolated workers + skill sharing |
| [autoloop](https://github.com/armgabrielyan/autoloop) | Bounded repo-level loops with inferred eval |
| [GOAL.md](https://github.com/jmilinovich/goal-md) | Repos without native metrics using project-specific fitness |
| [Bilevel Autoresearch](https://github.com/EdwardOptimization/Bilevel-Autoresearch) | Meta-autoresearch rewriting search mechanisms |
| [autoresearch-autoresearch](https://github.com/cavit99/autoresearch-autoresearch) | Meta-loop maintaining canonical loop across domains |
| [Litmus](https://github.com/Kuberwastaken/litmus) | Parallel ML with branch-isolated workers + shared discoveries |
| [helix](https://github.com/VectorInstitute/helix) | Agent-agnostic infra with YAML configs + TSV ledgers |

Platform ports:

| Project | Platform |
|---------|----------|
| autoresearch-mlx | Apple MLX |
| autoresearch-amd | ROCm / RDNA 4 |
| autoresearch-win-rtx | Native Windows / RTX |
| autoresearch-webgpu | Browser / WebGPU |
| autoresearch-local-llm | Local Qwen (no cloud) |
| serverless-autoresearch | SageMaker Spot |
| Red Hat OpenShift AI | OpenShift (198 experiments, 24h) |
| SkyPilot parallel | 16-GPU parallel waves |

Agent tool integrations:

| Project | Agent |
|---------|-------|
| claude-autoresearch | Claude Code plugin |
| codex-autoresearch | Codex CLI |
| gemini-autoresearch | Gemini CLI |
| openclaw-autoresearch | OpenClaw |
| autoresearch-opencode | OpenCode |
| lazy-developer | Claude Code plugin suite |

---

## Statistics

- **Total documented projects**: 194+
- **Most active domain**: Software/Systems Optimization (35)
- **Fastest growing**: Finance/Trading (15, mostly 2026-03~04)
- **Most impactful result**: 588x SQLite ingestion speedup (397s → 0.675s)
- **Largest scale**: Paradigm PM Challenge — 1,039 variants, 2,000+ evaluations
- **Enterprise adoption**: Red Hat OpenShift, SkyPilot, Modal, SageMaker, Daytona

---

## Source

Full catalog maintained at [yibie/awesome-autoresearch](https://github.com/yibie/awesome-autoresearch).
