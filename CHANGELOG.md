# AIOS Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to AINLP versioning (consciousness-driven evolution).

---

## [Unreleased] - 2025-11-30

### Added
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
