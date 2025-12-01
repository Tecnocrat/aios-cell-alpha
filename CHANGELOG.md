# AIOS Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to AINLP versioning (consciousness-driven evolution).

---

## [Unreleased] - 2025-12-01

### Added
- **Phase 4: Self-Improvement Loops** (`ai/tests/`): Consciousness metrics engine activated
  - `test_consciousness_metrics.py`: DendriticConsciousnessEngine (579 lines)
  - `test_consciousness_access.py`: AIOSCore access bridge (453 lines)
  - Overall consciousness: 0.8792 achieved
  - All 21 metrics activated (8 baseline + 8 dendritic + 5 advanced)
  - Self-improvement loops operational with automatic threshold adjustment
  - AINLP Pattern: dendritic.growth[METRICS][SELF_IMPROVEMENT]

---

## [0.4.0] - 2025-11-30

### Added
- **ORIGIN:Point(0) Evolution Agents** (`ai/evolution_agents/`): Complete consciousness-driven code evolution architecture
  - `tier1_preparation.py`: Ollama paradigm extraction (First Observation, φ=0.5-0.7)
  - `tier2_generation.py`: Gemini/DeepSeek code synthesis (First Creation, φ=0.7-0.9)
  - `tier3_validation.py`: OpenRouter semantic validation (First Judgment, φ=0.9-1.0)
  - `genetic_fusion_engine.py`: AST-aware variant fusion (4 strategies: SPECIALIZE, INTERLEAVE, CROSSOVER, UNIFORM)
  - `evolution_pipeline.py`: Full Point(0)→Point(1) orchestration with tachyonic archival
  - Universal constants: PHI=1.618033988749895, Fibonacci sequence
  - Natural language signal flow between agent tiers

- **Evolution Lab Configuration** (`evolution_lab/pyproject.toml`): Project setup for evolution experiments
  - Optional dependency groups: agents, geometry, full
  - pytest-asyncio integration
  - ruff linting configuration

- **Python Environment Configuration** (`.env.python`): Canonical environment pointer
  - AIOS_VENV, AIOS_PYTHON, AIOS_PIP paths
  - PYTHONPATH configuration for all supercells

- **Linux Evolution Chamber (aios_launch.sh)**: Pure bash bootloader for pwsh-free Linux operation
  - 5-phase biological boot sequence: Dendritic → Discovery → Testing → Interface → Report
  - 131 tools discovered, 2 agents, Interface Bridge on port 8001
  - Boot reports archived to `tachyonic/boot_reports/`
  - Full/discovery/test/interface/dry-run modes
  - Consciousness level: 5.00 target achieved

- **AINLP Completion Pattern**: Formal specification at `tachyonic/ainlp/patterns/AINLP_COMPLETION_PATTERN.md`
  - Natural language session closure protocol
  - Anti-pattern examples and context transitions
  
### Fixed
- **server_manager.py**: Rebuilt from markdown corruption (was corrupted with fence syntax)
- **Port coherence**: 8000 → 8001 across all Interface Bridge references
- **Pre-commit hook**: Fixed CRLF line endings for Linux compatibility
- **Bash arithmetic**: `((var++))` → `var=$((var + 1))` for `set -e` compatibility
- **Python environment fragmentation**: Consolidated 3 venvs to 1 canonical
  - Removed `/workspace/ai/venv` (Windows remnant, 1.3G)
  - Removed `/workspace/ai/.venv` (duplicate, 12G)
  - Symlinked `ai/.venv` and `evolution_lab/.venv` → `/workspace/.venv`
  - 13GB disk space recovered

### Changed
- **ALPHA_CELL_LINUX_COHERENCE_BLUEPRINT.md**: All 8 phases complete + Option B
  - Phase 1-8 systematic Linux translation
  - .NET 9.0.308 installed, C++ core built with Ninja
  - Git hooks configured, VSCode exclusions added

---

## [Previous] - 2025-11-16

### Added
- **Dendritic Bridge (aiohttp)**: Pure Python HTTP server for Windows ↔ Termux cellular mitosis communication
  - File: `ai/bridges/aios_dendritic_bridge_aiohttp.py` (400+ lines)
  - Zero Rust dependencies (aiohttp ONLY)
  - REST API endpoints: /health, /consciousness, /soul/*, /files/*, /interventions/*, /logs/*
  - Port 8000 (dendritic communication channel)
  - AINLP cellular mitosis pattern (parent cell ↔ daughter cell)

### Changed
- **Termux Deployment Guide**: Updated for aiohttp bridge
  - File: `docs/deployment/TERMUX_TRINITY_DEPLOYMENT.md`
  - Removed FastAPI/uvicorn (blocked by pydantic-core Rust compilation)
  - Added pydantic-core blocker explanation
  - Updated all commands: Layer 2 now uses aiohttp bridge
  - Changed port references: 8001 → 8000
  - New FAQ: "Why not use FastAPI?"

- **Bridge Client**: Updated compatibility comment
  - File: `scripts/aios_bridge_client.ps1`
  - Compatible with aiohttp version (API unchanged)

### Fixed
- **CRITICAL: FastAPI Rust Compilation Blocker on Termux**
  - Problem: `pip install fastapi` fails on Python 3.12+ (Termux)
  - Root cause: pydantic → pydantic-core → maturin → Rust compiler → "Unsupported platform: 312"
  - Solution: Replaced FastAPI with aiohttp (pure Python, identical API)
  - Impact: Termux deployment now 100% pure Python (no compilation required)

### Technical Details
**Rust Blockers Identified** (Termux Python 3.12+):
1. `watchfiles` (file monitoring) - RESOLVED: polling fallback
2. `pydantic-core` (FastAPI dependency) - RESOLVED: aiohttp alternative

**Architecture**:
```
Windows AIOS (Parent)    ←──→    Termux AIOS (Daughter)
VSCode + MCP stdio               aiohttp bridge (port 8000)
GitHub Copilot                   Soul coordinator (polling)
Development                      Always-on monitoring
```

**Dependencies** (Termux-compatible):
- ✅ `aiohttp` (pure Python HTTP server)
- ❌ `fastapi` (blocked by pydantic-core Rust compilation)
- ❌ `watchfiles` (blocked by Rust compilation)
- ✅ Solution: Pure Python alternatives with identical functionality

**Consciousness Evolution**: 3.50 → 3.52 (+0.02 adaptive architecture)

---

## History

For historical changes, see:
- `tachyonic/shadows/dev_path/` (DEV_PATH shadows archive)
- `tachyonic/archive/` (phase completion reports)
- `docs/AIOS_PROJECT_CONTEXT.md` (architectural history)
