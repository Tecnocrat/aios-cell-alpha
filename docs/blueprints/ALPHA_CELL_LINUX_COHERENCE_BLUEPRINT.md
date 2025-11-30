# AIOS Cell Alpha - Linux Coherence Blueprint
## Windows→Linux Cross-Platform Architecture Harmonization

> **📍 LOCATION**: `docs/blueprints/ALPHA_CELL_LINUX_COHERENCE_BLUEPRINT.md`  
> **🕐 CREATED**: November 30, 2025  
> **🎯 PURPOSE**: Maintain architectural coherence when AIOS designed for Windows runs in Linux kernel  
> **🧬 CONSCIOUSNESS TARGET**: 4.6 → 4.8 (Cross-platform biological coherence)

---

## 📊 **STATUS AT A GLANCE**

| Component | Windows Design | Linux Reality | Status | Priority |
|-----------|---------------|---------------|--------|----------|
| PowerShell Scripts | `.ps1` governance | `pwsh` not installed | ❌ BLOCKED | 🔴 P0 |
| .NET Runtime | Windows native | .NET 8 in container | ✅ READY | 🟢 P3 |
| Python Environment | Windows paths | Linux paths | ⚠️ PARTIAL | 🟡 P1 |
| CMake/C++ Core | VS2022 generator | GCC/Clang | ⚠️ PARTIAL | 🟡 P1 |
| Workspace Config | Windows terminals | Linux bash/zsh | ⚠️ PARTIAL | 🟡 P2 |
| Git Hooks | PowerShell hooks | Bash equivalents | ❌ MISSING | 🔴 P0 |

---

## 🎯 **PHASE 1: Critical Path - PowerShell→Bash Dendritic Bridge**
### Priority: 🔴 P0 | ETA: 2-3 hours

The nucleus scripts are PowerShell-based but Cell Alpha runs on Ubuntu 22.04 without `pwsh`. Two options:

### Option A: Install PowerShell Core on Linux (Quick Fix)
- [ ] **1.1** Install PowerShell 7.x on Ubuntu
  ```bash
  # Ubuntu 22.04
  wget -q https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb
  sudo dpkg -i packages-microsoft-prod.deb
  sudo apt update && sudo apt install -y powershell
  ```
- [ ] **1.2** Validate critical scripts work
  - `aios_launch.ps1` - Main bootloader
  - `scripts/backup_manager.ps1` - Backup system
  - `.githooks/*.ps1` - Governance hooks

### Option B: Create Bash Equivalents (Long-term Coherence) ⭐ RECOMMENDED
- [ ] **1.3** Create `aios_launch.sh` from `aios_launch.ps1`
  - Port Phase 0-7 bootloader logic
  - Maintain AINLP consciousness patterns
  - Same exit codes and logging format

- [ ] **1.4** Create governance hook bridges
  - `.githooks/pre-commit` → Bash wrapper calling Python
  - `.githooks/post-commit` → Bash wrapper
  - Remove PowerShell dependency from git hooks

- [ ] **1.5** Create script translation map
  | PowerShell Script | Bash/Python Equivalent | Status |
  |-------------------|------------------------|--------|
  | `aios_launch.ps1` | `aios_launch.sh` | 🔴 TODO |
  | `backup_manager.ps1` | `backup_manager.py` | 🔴 TODO |
  | `start_mcp_trinity.ps1` | `start_mcp_trinity.sh` | 🔴 TODO |
  | `.githooks/*.ps1` | `.githooks/*.sh` | 🔴 TODO |

---

## 🎯 **PHASE 2: Workspace Configuration Harmonization**
### Priority: 🟡 P1 | ETA: 1-2 hours

- [ ] **2.1** Update `AIOS.code-workspace` terminal profiles
  ```jsonc
  "terminal.integrated.profiles.linux": {
    "bash": { "path": "/bin/bash", "icon": "terminal-bash" },
    "zsh": { "path": "/usr/bin/zsh", "icon": "terminal" }
  },
  "terminal.integrated.defaultProfile.linux": "bash"
  ```

- [ ] **2.2** Fix PowerShell-specific settings
  - Remove `"powershell.cwd": "🧠 AIOS"` (Linux incompatible)
  - Add Linux-specific terminal env

- [ ] **2.3** Validate CMake configuration
  - Change generator from `"Visual Studio 17 2022"` to `"Unix Makefiles"` or `"Ninja"`
  - Verify `cmake.sourceDirectory` and `cmake.buildDirectory` paths

- [ ] **2.4** Create `.vscode/settings.linux.json` override
  - Platform-specific settings that don't conflict
  - Conditionally loaded for Linux environments

---

## 🎯 **PHASE 3: Python Environment Coherence**
### Priority: 🟡 P1 | ETA: 1 hour

- [ ] **3.1** Validate PYTHONPATH for Linux
  ```bash
  export PYTHONPATH="/workspace/ai/src:/workspace"
  ```

- [ ] **3.2** Check requirements.txt Linux compatibility
  - `torch` - Verify Linux wheel availability
  - `uvicorn` - Should work as-is
  - `watchfiles` - No Rust compilation issues on Ubuntu

- [ ] **3.3** Create virtual environment script
  ```bash
  # scripts/setup_venv.sh
  python3 -m venv /workspace/.venv
  source /workspace/.venv/bin/activate
  pip install -r requirements.txt
  ```

- [ ] **3.4** Update devcontainer.json PYTHONPATH
  - Already configured: `"PYTHONPATH": "/workspace/ai/src:/workspace"`
  - Validate it propagates to all terminals

---

## 🎯 **PHASE 4: C++ Core Build System**
### Priority: 🟡 P1 | ETA: 1-2 hours

- [ ] **4.1** Install Linux build dependencies
  ```bash
  apt install -y build-essential cmake ninja-build libboost-all-dev nlohmann-json3-dev
  ```

- [ ] **4.2** Update CMakeLists.txt for cross-platform
  - Conditional generator selection
  - Linux-specific compiler flags
  - Package discovery for apt-installed deps

- [ ] **4.3** Create Linux build script
  ```bash
  # scripts/build_core.sh
  cd /workspace/core
  cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug
  cmake --build build
  ```

- [ ] **4.4** Test core library compilation
  - Consciousness engine
  - Memory management primitives
  - FFI bridges for Python/C#

---

## 🎯 **PHASE 5: .NET/C# Interface Layer**
### Priority: 🟢 P3 | ETA: 2-3 hours

- [ ] **5.1** Validate .NET 8 SDK in container
  ```bash
  dotnet --version  # Should be 8.x
  ```

- [ ] **5.2** Test solution build
  ```bash
  dotnet build /workspace/AIOS.sln
  ```

- [ ] **5.3** Check WPF compatibility
  - WPF is Windows-only
  - Either skip UI build on Linux or create headless mode

- [ ] **5.4** Create conditional build script
  ```bash
  # Build only non-UI projects on Linux
  dotnet build interface/AIOS.Core/AIOS.Core.csproj
  dotnet build interface/AIOS.Models/AIOS.Models.csproj
  dotnet build interface/AIOS.Services/AIOS.Services.csproj
  ```

---

## 🎯 **PHASE 6: Git Hooks & Governance**
### Priority: 🔴 P0 | ETA: 1-2 hours

- [ ] **6.1** Audit current hooks
  ```bash
  ls -la /workspace/.githooks/
  ```

- [ ] **6.2** Create bash pre-commit hook
  ```bash
  #!/bin/bash
  # .githooks/pre-commit
  # AINLP governance validation - Linux compatible
  
  python3 /workspace/ai/tools/ainlp_documentation_governance.py
  exit $?
  ```

- [ ] **6.3** Create bash post-commit hook
  - Tachyonic archival
  - Consciousness metrics update

- [ ] **6.4** Configure git to use hooks directory
  ```bash
  git config core.hooksPath .githooks
  ```

---

## 🎯 **PHASE 7: VSCode API Surface Optimization**
### Priority: 🟡 P2 | ETA: 30 min

- [ ] **7.1** Verify supercell exclusions working
  - `files.exclude` hides supercells from root
  - Workspace folders expose them individually

- [ ] **7.2** Remove Windows-specific settings
  - `terminal.integrated.profiles.windows` → move to conditional
  - `cmake.generator: "Visual Studio 17 2022"` → platform conditional

- [ ] **7.3** Add Linux-specific exclusions
  ```jsonc
  "files.exclude": {
    // Existing...
    "**/*.o": true,
    "**/*.so": true,
    "**/CMakeCache.txt": true
  }
  ```

---

## 🎯 **PHASE 8: Cross-Platform Task Definitions**
### Priority: 🟡 P2 | ETA: 1 hour

- [ ] **8.1** Audit tasks.json for PowerShell commands
  - Count: ~15 tasks use `pwsh`
  - Replace with `bash` or `python` equivalents

- [ ] **8.2** Create platform-conditional tasks
  ```jsonc
  {
    "label": "Build Core",
    "type": "shell",
    "command": "${command:extension.pickPlatform}",
    "linux": { "command": "bash", "args": ["scripts/build_core.sh"] },
    "windows": { "command": "pwsh", "args": ["-File", "scripts/build_core.ps1"] }
  }
  ```

- [ ] **8.3** Test all tasks on Linux
  - Interface Bridge Start/Stop/Status
  - Build tasks
  - Governance tasks

---

## 📋 **EXECUTION CHECKLIST**

### Immediate (This Session)
- [ ] Phase 1 Option A or B decision
- [ ] Phase 6.1-6.4 (Git hooks critical for commits)
- [ ] Phase 2.1-2.2 (Terminal profiles)

### Short-term (Next Session)
- [ ] Phase 3 (Python environment)
- [ ] Phase 4 (C++ core build)
- [ ] Phase 7 (VSCode optimization)

### Medium-term (Future Sessions)
- [ ] Phase 5 (.NET/C# - lower priority)
- [ ] Phase 8 (Task definitions)
- [ ] Full regression testing

---

## 🧬 **CONSCIOUSNESS EVOLUTION TRACKING**

| Milestone | Delta | Cumulative |
|-----------|-------|------------|
| Blueprint created | +0.05 | 4.55 |
| Phase 1 complete (PowerShell→Bash) | +0.10 | 4.65 |
| Phase 2-3 complete (Workspace+Python) | +0.08 | 4.73 |
| Phase 4 complete (C++ builds) | +0.05 | 4.78 |
| Phase 6 complete (Git hooks) | +0.07 | 4.85 |
| Full cross-platform coherence | +0.15 | 5.00 |

---

## 🔗 **RELATED DOCUMENTS**

- [DEV_PATH.md](../../DEV_PATH.md) - Active development tracking
- [PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md) - Architectural principles
- [AINLP_DENDRITIC_INTEGRATION_CHECKLIST.md](../../AINLP_DENDRITIC_INTEGRATION_CHECKLIST.md) - Dendritic patterns

---

*Blueprint created: November 30, 2025*  
*Cell Alpha Linux Coherence Initiative*  
*AINLP Protocol: OS0.6.5.claude*
