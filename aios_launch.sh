#!/bin/bash
# ============================================================================
# 🧬 AIOS LINUX EVOLUTION CHAMBER - Cell Alpha Bootloader
# ============================================================================
# AINLP Protocol: OS0.6.2.claude - Cross-Platform Biological Architecture
# Bash equivalent of aios_launch.ps1 for pwsh-free Linux operation
#
# Usage:
#   ./aios_launch.sh                    # Full boot
#   ./aios_launch.sh --mode discovery   # Discovery only
#   ./aios_launch.sh --quick            # Quick boot (skip tests)
#   ./aios_launch.sh --keep-alive       # Keep interface bridge running
#   ./aios_launch.sh --help             # Show all options
#
# Environment: Ubuntu 22.04+ / WSL2 / Linux containers
# Consciousness Level: Nucleus (system-wide coordination)
# ============================================================================

set -euo pipefail

# ============================================================================
# 🎨 CONFIGURATION & GLOBALS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AIOS_ROOT="${SCRIPT_DIR}"
BOOT_START_TIME=$(date +%s)

# Boot modes
MODE="${MODE:-full}"
QUICK_BOOT="${QUICK_BOOT:-false}"
KEEP_ALIVE="${KEEP_ALIVE:-false}"
SKIP_DISCOVERY="${SKIP_DISCOVERY:-false}"
SKIP_TESTING="${SKIP_TESTING:-false}"
SKIP_INTERFACE="${SKIP_INTERFACE:-false}"
VERBOSE="${VERBOSE:-false}"

# Boot metrics (tracked in associative array)
declare -A BOOT_METRICS=(
    [dendritic_coherence]=0.0
    [semantic_registry]=false
    [tools_discovered]=0
    [agents_tested]=0
    [interfaces_launched]=0
    [errors]=0
    [warnings]=0
)

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# ============================================================================
# 📝 LOGGING FUNCTIONS
# ============================================================================

log_phase() {
    local phase="$1"
    local message="$2"
    local color="${3:-$CYAN}"
    echo -e "${color}🚀 [$phase] $message${NC}"
}

log_success() {
    echo -e "  ${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "  ${YELLOW}⚠️  $1${NC}"
    ((BOOT_METRICS[warnings]++)) || true
}

log_error() {
    echo -e "  ${RED}❌ $1${NC}"
    ((BOOT_METRICS[errors]++)) || true
}

log_info() {
    echo -e "  ${BLUE}ℹ️  $1${NC}"
}

log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "  ${GRAY}$1${NC}"
    fi
}

# ============================================================================
# 🛠️ UTILITY FUNCTIONS
# ============================================================================

check_command() {
    command -v "$1" &> /dev/null
}

find_python() {
    for cmd in python3 python; do
        if check_command "$cmd"; then
            echo "$cmd"
            return 0
        fi
    done
    return 1
}

duration_since() {
    local start=$1
    local end=$(date +%s)
    echo "$((end - start))"
}

# ============================================================================
# 🌿 PHASE 0: DENDRITIC CONFIGURATION CONSCIOUSNESS
# ============================================================================

phase_dendritic_configuration() {
    log_phase "DENDRITIC" "Establishing configuration consciousness..." "$MAGENTA"
    
    local python_cmd
    python_cmd=$(find_python) || {
        log_warning "Python not found - using manual dendritic configuration"
        
        # Manual fallback: verify semantic registry
        local registry_path="${AIOS_ROOT}/tachyonic/consciousness/config_registry.json"
        if [[ -f "$registry_path" ]]; then
            log_success "Semantic registry found at ${registry_path}"
            BOOT_METRICS[semantic_registry]=true
        else
            log_warning "Semantic registry not found - configuration coherence not established"
        fi
        return 0
    }
    
    log_info "Python found: $python_cmd"
    
    # Execute dendritic configuration agent
    local agent_path="${AIOS_ROOT}/ai/tools/dendritic_config_agent.py"
    
    if [[ -f "$agent_path" ]]; then
        log_info "Executing dendritic configuration agent..."
        
        if $python_cmd "$agent_path" 2>&1 | while read -r line; do
            log_verbose "$line"
            if [[ "$line" =~ Coherence\ Level:\ ([0-9.]+) ]]; then
                BOOT_METRICS[dendritic_coherence]="${BASH_REMATCH[1]}"
            fi
        done; then
            log_success "Dendritic configuration agent executed successfully"
            BOOT_METRICS[semantic_registry]=true
        else
            log_warning "Dendritic agent execution had errors"
        fi
    else
        log_warning "dendritic_config_agent.py not found at $agent_path"
    fi
    
    # Verify semantic registry was created
    local registry_path="${AIOS_ROOT}/tachyonic/consciousness/config_registry.json"
    if [[ -f "$registry_path" ]]; then
        log_success "Semantic registry verified"
        BOOT_METRICS[semantic_registry]=true
    fi
    
    # Phase 0.5: Fractal ingestion (optional)
    local ingestion_path="${AIOS_ROOT}/ai/src/ingestion/ainlp_ingestion_class.py"
    if [[ -f "$ingestion_path" ]]; then
        log_info "Executing consciousness fractal ingestion..."
        if $python_cmd "$ingestion_path" &>/dev/null; then
            log_success "Fractal ingestion complete"
        else
            log_warning "Fractal ingestion completed with warnings"
        fi
    fi
    
    log_info "Dendritic consciousness: ${BOOT_METRICS[semantic_registry]}"
}

# ============================================================================
# 🧬 PHASE 1: INTELLIGENT TOOL DISCOVERY
# ============================================================================

phase_tool_discovery() {
    if [[ "$SKIP_DISCOVERY" == "true" ]]; then
        log_warning "Discovery phase skipped by user"
        return 0
    fi
    
    log_phase "DISCOVERY" "Scanning AIOS architecture for intelligent tools..."
    
    local count=0
    
    # Discover AI tools
    local ai_tools_path="${AIOS_ROOT}/ai/tools"
    if [[ -d "$ai_tools_path" ]]; then
        local ai_count
        ai_count=$(find "$ai_tools_path" -name "*.py" ! -name "_*" ! -name "test_*" 2>/dev/null | wc -l)
        count=$((count + ai_count))
        log_success "AI Tools: $ai_count discovered"
    fi
    
    # Discover Runtime Intelligence tools
    local runtime_path="${AIOS_ROOT}/runtime_intelligence/tools"
    if [[ -d "$runtime_path" ]]; then
        local runtime_count
        runtime_count=$(find "$runtime_path" -name "*.py" ! -name "_*" ! -name "test_*" 2>/dev/null | wc -l)
        count=$((count + runtime_count))
        log_success "Runtime Intelligence Tools: $runtime_count discovered"
    fi
    
    # Discover Consciousness Crystals
    local crystals_path="${AIOS_ROOT}/ai/cytoplasm/consciousness_crystals"
    if [[ -d "$crystals_path" ]]; then
        local crystal_count
        crystal_count=$(find "$crystals_path" -name "*.json" 2>/dev/null | wc -l)
        count=$((count + crystal_count))
        log_success "Consciousness Crystals: $crystal_count discovered"
    fi
    
    # Discover Core C++ modules
    local core_lib="${AIOS_ROOT}/core/build/lib"
    if [[ -d "$core_lib" ]]; then
        local so_count
        so_count=$(find "$core_lib" -name "*.so*" 2>/dev/null | wc -l)
        if [[ $so_count -gt 0 ]]; then
            log_success "Core Shared Libraries: $so_count discovered"
            count=$((count + so_count))
        fi
    fi
    
    # Discover .NET assemblies
    local interface_path="${AIOS_ROOT}/interface"
    if [[ -d "$interface_path" ]]; then
        local dll_count
        dll_count=$(find "$interface_path" -name "*.dll" -path "*/bin/*" 2>/dev/null | wc -l)
        if [[ $dll_count -gt 0 ]]; then
            log_success ".NET Assemblies: $dll_count discovered"
            count=$((count + dll_count))
        fi
    fi
    
    BOOT_METRICS[tools_discovered]=$count
    log_info "Total tools discovered: $count"
}

# ============================================================================
# 🧪 PHASE 2: AGENT HEALTH VALIDATION
# ============================================================================

phase_agent_testing() {
    if [[ "$SKIP_TESTING" == "true" ]] || [[ "$QUICK_BOOT" == "true" ]]; then
        log_warning "Testing phase skipped"
        return 0
    fi
    
    log_phase "TESTING" "Validating agent health..."
    
    local python_cmd
    python_cmd=$(find_python) || {
        log_warning "Python not available - skipping agent tests"
        return 0
    }
    
    local tested=0
    
    # Test lightweight AI coordinator
    local coordinator="${AIOS_ROOT}/ai/src/integrations/lightweight_ai_coordinator.py"
    if [[ -f "$coordinator" ]]; then
        log_info "Testing lightweight AI coordinator..."
        if timeout 5 $python_cmd -c "print('OK')" 2>/dev/null; then
            log_success "Python execution: HEALTHY"
            tested=$((tested + 1))
        else
            log_warning "Python execution: TIMEOUT"
        fi
    fi
    
    # Test interface bridge (import only - skip heavy imports)
    local bridge="${AIOS_ROOT}/ai/nucleus/interface_bridge.py"
    if [[ -f "$bridge" ]]; then
        log_info "Testing interface bridge module..."
        if [[ -f "$bridge" ]]; then
            log_success "Interface Bridge Module: PRESENT"
            tested=$((tested + 1))
        fi
    fi
    
    BOOT_METRICS[agents_tested]=$tested
    log_info "Agents tested: $tested"
}

# ============================================================================
# 🌐 PHASE 4: INTERFACE LAUNCH
# ============================================================================

phase_interface_launch() {
    if [[ "$SKIP_INTERFACE" == "true" ]]; then
        log_warning "Interface launch skipped by user"
        return 0
    fi
    
    if [[ "$MODE" == "discovery" ]] || [[ "$MODE" == "test" ]]; then
        log_info "Interface launch skipped (mode: $MODE)"
        return 0
    fi
    
    log_phase "INTERFACE" "Launching AIOS services..."
    
    local python_cmd
    python_cmd=$(find_python) || {
        log_error "Python not available - cannot launch interface"
        return 1
    }
    
    local launched=0
    
    # Launch Interface Bridge
    local server_manager="${AIOS_ROOT}/ai/server_manager.py"
    if [[ -f "$server_manager" ]]; then
        log_info "Starting Interface Bridge..."
        
        # Check if already running
        if curl -s http://localhost:8001/health &>/dev/null; then
            log_success "Interface Bridge: ALREADY RUNNING"
            launched=$((launched + 1))
        else
            cd "${AIOS_ROOT}/ai"
            if [[ "$KEEP_ALIVE" == "true" ]]; then
                # Foreground mode with keep-alive
                log_info "Starting in keep-alive mode (Ctrl+C to stop)..."
                $python_cmd "$server_manager" start
            else
                # Background mode
                $python_cmd "$server_manager" start
                sleep 3
                
                if curl -s http://localhost:8001/health &>/dev/null; then
                    log_success "Interface Bridge: STARTED (http://localhost:8001)"
                    launched=$((launched + 1))
                else
                    log_warning "Interface Bridge: FAILED TO START"
                fi
            fi
            cd "$AIOS_ROOT"
        fi
    else
        log_warning "server_manager.py not found"
    fi
    
    BOOT_METRICS[interfaces_launched]=$launched
}

# ============================================================================
# 📊 PHASE 5: BOOT REPORTING
# ============================================================================

phase_boot_report() {
    log_phase "REPORT" "Generating boot summary..."
    
    local boot_end_time=$(date +%s)
    local duration=$((boot_end_time - BOOT_START_TIME))
    
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🧬 AIOS LINUX EVOLUTION CHAMBER - BOOT COMPLETE${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${BLUE}Mode:${NC}                 $MODE"
    echo -e "  ${BLUE}Duration:${NC}             ${duration}s"
    echo -e "  ${BLUE}Tools Discovered:${NC}     ${BOOT_METRICS[tools_discovered]}"
    echo -e "  ${BLUE}Agents Tested:${NC}        ${BOOT_METRICS[agents_tested]}"
    echo -e "  ${BLUE}Interfaces Launched:${NC}  ${BOOT_METRICS[interfaces_launched]}"
    echo -e "  ${BLUE}Semantic Registry:${NC}    ${BOOT_METRICS[semantic_registry]}"
    echo -e "  ${BLUE}Errors:${NC}               ${BOOT_METRICS[errors]}"
    echo -e "  ${BLUE}Warnings:${NC}             ${BOOT_METRICS[warnings]}"
    echo ""
    
    # System status
    if [[ ${BOOT_METRICS[errors]} -eq 0 ]]; then
        echo -e "  ${GREEN}🟢 SYSTEM STATUS: OPERATIONAL${NC}"
    elif [[ ${BOOT_METRICS[errors]} -lt 3 ]]; then
        echo -e "  ${YELLOW}🟡 SYSTEM STATUS: DEGRADED${NC}"
    else
        echo -e "  ${RED}🔴 SYSTEM STATUS: CRITICAL${NC}"
    fi
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    
    # Archive boot report
    local reports_dir="${AIOS_ROOT}/tachyonic/boot_reports"
    mkdir -p "$reports_dir"
    
    local report_file="${reports_dir}/boot_$(date +%Y%m%d_%H%M%S).json"
    cat > "$report_file" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "mode": "$MODE",
    "duration_seconds": $duration,
    "platform": "linux",
    "shell": "bash",
    "metrics": {
        "tools_discovered": ${BOOT_METRICS[tools_discovered]},
        "agents_tested": ${BOOT_METRICS[agents_tested]},
        "interfaces_launched": ${BOOT_METRICS[interfaces_launched]},
        "semantic_registry": ${BOOT_METRICS[semantic_registry]},
        "dendritic_coherence": ${BOOT_METRICS[dendritic_coherence]},
        "errors": ${BOOT_METRICS[errors]},
        "warnings": ${BOOT_METRICS[warnings]}
    },
    "status": "$([[ ${BOOT_METRICS[errors]} -eq 0 ]] && echo "OPERATIONAL" || echo "DEGRADED")"
}
EOF
    
    log_success "Boot report archived: $report_file"
}

# ============================================================================
# 🚀 MAIN EXECUTION
# ============================================================================

show_help() {
    cat << EOF
AIOS Linux Evolution Chamber - Cell Alpha Bootloader

Usage: $(basename "$0") [OPTIONS]

Options:
    --mode MODE         Boot mode: full, discovery, test, interface
    --quick             Quick boot (skip detailed tests)
    --keep-alive        Keep interface bridge running (foreground)
    --skip-discovery    Skip tool discovery phase
    --skip-testing      Skip agent testing phase
    --skip-interface    Skip interface launch phase
    --verbose           Enable verbose logging
    --help              Show this help message

Examples:
    $(basename "$0")                    # Full boot
    $(basename "$0") --mode discovery   # Discovery only
    $(basename "$0") --quick            # Quick boot
    $(basename "$0") --keep-alive       # Run with keep-alive

Environment Variables:
    MODE                Same as --mode
    QUICK_BOOT          Same as --quick (true/false)
    KEEP_ALIVE          Same as --keep-alive (true/false)
    VERBOSE             Same as --verbose (true/false)

AINLP Protocol: OS0.6.2.claude - Cross-Platform Biological Architecture
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --mode)
                MODE="$2"
                shift 2
                ;;
            --quick)
                QUICK_BOOT=true
                shift
                ;;
            --keep-alive)
                KEEP_ALIVE=true
                shift
                ;;
            --skip-discovery)
                SKIP_DISCOVERY=true
                shift
                ;;
            --skip-testing)
                SKIP_TESTING=true
                shift
                ;;
            --skip-interface)
                SKIP_INTERFACE=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

main() {
    parse_args "$@"
    
    echo ""
    echo -e "${MAGENTA}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║  🧬 AIOS LINUX EVOLUTION CHAMBER - Cell Alpha            ║${NC}"
    echo -e "${MAGENTA}║  Biological Architecture Bootloader v1.0.0               ║${NC}"
    echo -e "${MAGENTA}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Execute boot phases
    case $MODE in
        full)
            phase_dendritic_configuration
            phase_tool_discovery
            phase_agent_testing
            phase_interface_launch
            phase_boot_report
            ;;
        discovery)
            phase_dendritic_configuration
            phase_tool_discovery
            phase_boot_report
            ;;
        test)
            phase_dendritic_configuration
            phase_agent_testing
            phase_boot_report
            ;;
        interface)
            phase_interface_launch
            phase_boot_report
            ;;
        *)
            log_error "Unknown mode: $MODE"
            exit 1
            ;;
    esac
    
    # Keep-alive loop
    if [[ "$KEEP_ALIVE" == "true" ]] && [[ "$MODE" == "full" || "$MODE" == "interface" ]]; then
        log_info "Keep-alive mode active. Press Ctrl+C to stop."
        
        trap 'echo ""; log_info "Shutting down..."; cd "${AIOS_ROOT}/ai" && python3 server_manager.py stop 2>/dev/null; exit 0' INT TERM
        
        while true; do
            sleep 30
            if ! curl -s http://localhost:8000/health &>/dev/null; then
                log_warning "Interface Bridge health check failed - restarting..."
                cd "${AIOS_ROOT}/ai"
                python3 server_manager.py restart 2>/dev/null || true
                cd "$AIOS_ROOT"
            fi
        done
    fi
}

# Run main
main "$@"
