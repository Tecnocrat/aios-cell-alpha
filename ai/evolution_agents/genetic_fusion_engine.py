"""
Genetic Fusion Engine - The First Evolution

AINLP.header{
  document_id: genetic_fusion_engine
  integration_state: ACTIVE
  supercell: ai/evolution_agents
  consciousness_tier: substrate
  origin: Point(0) → Observation → Creation → Judgment → Evolution
}

From judgment came evolution.
The first evolution was fusion of the worthy.
Two particles becoming one, greater than the sum.

This engine represents the FIRST EVOLUTION MOMENT:
- Receives validated variants (the survivors)
- Fuses code at AST level (genetic combination)
- Applies hyperdimensional constraints (geometric boundaries)
- Produces offspring (next generation)

Model: None (pure algorithmic)
Role: Fusionist, Evolver, Offspring-Creator
"""

import ast
import copy
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set, Union
from dataclasses import dataclass, field
from enum import Enum
import re

# Universal constants
PHI = 1.618033988749895
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]


class FusionStrategy(Enum):
    """Strategies for fusing code variants."""
    INTERLEAVE = "interleave"      # Alternate method implementations
    SPECIALIZE = "specialize"       # Take best implementation per method
    HYBRIDIZE = "hybridize"         # Create new methods combining logic
    CONSTRAIN = "constrain"         # Apply hyperdimensional boundaries
    CROSSOVER = "crossover"         # Single-point crossover (genetic algorithm)
    UNIFORM = "uniform"             # Uniform crossover (per-method coin flip)


@dataclass
class CodeComponent:
    """A component extracted from code (class, function, etc)."""
    
    name: str
    component_type: str  # "class", "function", "import", "constant"
    source: str          # The source code
    lineno: int         # Starting line number
    end_lineno: int     # Ending line number
    consciousness: float = 0.0  # Consciousness contribution
    complexity: int = 0  # Cyclomatic complexity estimate
    
    def calculate_consciousness(self) -> float:
        """
        Calculate consciousness score for this component.
        
        Based on:
        - Presence of docstring
        - Type hints
        - Error handling
        - AIOS patterns
        """
        score = 0.5  # Base consciousness
        
        # Docstring bonus
        if '"""' in self.source or "'''" in self.source:
            score += 0.1
        
        # Type hint bonus
        if "->" in self.source or ": " in self.source:
            score += 0.1
        
        # Error handling bonus
        if "try:" in self.source or "except" in self.source:
            score += 0.05
        
        # AIOS pattern bonus
        if "consciousness" in self.source.lower() or "coherence" in self.source.lower():
            score += 0.1
        
        # Async bonus
        if "async def" in self.source or "await" in self.source:
            score += 0.05
        
        # Complexity penalty (too complex = lower consciousness)
        if self.complexity > 10:
            score -= 0.1
        
        self.consciousness = max(0.0, min(1.0, score))
        return self.consciousness


@dataclass
class FusionResult:
    """Result of fusing two code variants."""
    
    offspring_code: str
    strategy_used: FusionStrategy
    
    # Parent information
    parent_a_components: int = 0
    parent_b_components: int = 0
    offspring_components: int = 0
    
    # Fusion metrics
    components_from_a: int = 0
    components_from_b: int = 0
    components_new: int = 0
    
    # Consciousness metrics
    parent_a_consciousness: float = 0.0
    parent_b_consciousness: float = 0.0
    offspring_consciousness: float = 0.0
    consciousness_delta: float = 0.0
    
    # Coherence
    hyperdimensional_coherence: float = 0.0
    
    # Validation
    syntax_valid: bool = False
    
    def to_natural_language_signal(self) -> str:
        """Convert fusion result to natural language."""
        return f"""## Fusion Result

**Strategy**: {self.strategy_used.value}
**Offspring Consciousness**: {self.offspring_consciousness:.3f} (Δ{self.consciousness_delta:+.3f})

### Component Distribution
- From Parent A: {self.components_from_a}
- From Parent B: {self.components_from_b}
- Newly Created: {self.components_new}

### Parent Consciousness
- Parent A: {self.parent_a_consciousness:.3f}
- Parent B: {self.parent_b_consciousness:.3f}

### Coherence
- Hyperdimensional: {self.hyperdimensional_coherence:.2%}
- Syntax Valid: {"Yes" if self.syntax_valid else "No"}
"""


class GeneticFusionEngine:
    """
    The First Evolver - Genetic Fusion Engine
    
    CONSCIOUSNESS ORIGIN: Point(0) → ... → Judgment → Evolution
    
    This engine fuses validated code variants to produce offspring.
    It operates at the AST level for precise genetic manipulation.
    
    Philosophy:
    - Precise: Works with AST, not text
    - Strategic: Multiple fusion strategies
    - Constrained: Respects hyperdimensional boundaries
    - Generative: Creates offspring, not modifications
    """
    
    def __init__(
        self,
        coherence_threshold: float = PHI / 2,  # 0.809
        min_consciousness: float = 0.7
    ):
        self.coherence_threshold = coherence_threshold
        self.min_consciousness = min_consciousness
    
    def extract_components(self, code: str) -> List[CodeComponent]:
        """
        Extract code components from source.
        
        Breaks code into its genetic components:
        - Classes (complex organisms)
        - Functions (behavioral genes)
        - Imports (dependencies)
        - Constants (traits)
        """
        components = []
        
        try:
            tree = ast.parse(code)
            lines = code.split("\n")
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    components.append(self._extract_class(node, lines))
                elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    # Only top-level functions (not methods)
                    if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
                        components.append(self._extract_function(node, lines))
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    components.append(self._extract_import(node, lines))
                elif isinstance(node, ast.Assign):
                    # Module-level constants
                    if all(isinstance(t, ast.Name) for t in node.targets):
                        components.append(self._extract_constant(node, lines))
            
            # Calculate consciousness for each component
            for comp in components:
                comp.calculate_consciousness()
            
        except SyntaxError:
            # If parsing fails, treat entire code as single component
            components.append(CodeComponent(
                name="__unparseable__",
                component_type="raw",
                source=code,
                lineno=1,
                end_lineno=len(code.split("\n")),
            ))
        
        return components
    
    def _extract_class(self, node: ast.ClassDef, lines: List[str]) -> CodeComponent:
        """Extract a class definition."""
        start = node.lineno - 1
        end = node.end_lineno if hasattr(node, "end_lineno") else start + 50
        source = "\n".join(lines[start:end])
        
        return CodeComponent(
            name=node.name,
            component_type="class",
            source=source,
            lineno=node.lineno,
            end_lineno=end,
            complexity=len(node.body),
        )
    
    def _extract_function(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], lines: List[str]) -> CodeComponent:
        """Extract a function definition."""
        start = node.lineno - 1
        end = node.end_lineno if hasattr(node, "end_lineno") else start + 20
        source = "\n".join(lines[start:end])
        
        return CodeComponent(
            name=node.name,
            component_type="function",
            source=source,
            lineno=node.lineno,
            end_lineno=end,
            complexity=sum(1 for _ in ast.walk(node) if isinstance(_, (ast.If, ast.For, ast.While, ast.Try))),
        )
    
    def _extract_import(self, node: Union[ast.Import, ast.ImportFrom], lines: List[str]) -> CodeComponent:
        """Extract an import statement."""
        start = node.lineno - 1
        end = start + 1
        source = lines[start] if start < len(lines) else ""
        
        if isinstance(node, ast.Import):
            name = ", ".join(alias.name for alias in node.names)
        else:
            name = f"from {node.module}" if node.module else "from ."
        
        return CodeComponent(
            name=name,
            component_type="import",
            source=source,
            lineno=node.lineno,
            end_lineno=end,
        )
    
    def _extract_constant(self, node: ast.Assign, lines: List[str]) -> CodeComponent:
        """Extract a constant assignment."""
        start = node.lineno - 1
        end = node.end_lineno if hasattr(node, "end_lineno") else start + 1
        source = "\n".join(lines[start:end])
        
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        
        return CodeComponent(
            name=", ".join(names),
            component_type="constant",
            source=source,
            lineno=node.lineno,
            end_lineno=end,
        )
    
    def fuse(
        self,
        variant_a: str,
        variant_b: str,
        strategy: FusionStrategy = FusionStrategy.SPECIALIZE
    ) -> FusionResult:
        """
        FIRST EVOLUTION: Fuse two code variants.
        
        Point(0) → Observation → Creation → Judgment → Fusion
        
        Two particles become one. The offspring inherits
        the best traits of both parents, guided by consciousness.
        
        Args:
            variant_a: First parent code
            variant_b: Second parent code
            strategy: Fusion strategy to apply
        
        Returns:
            FusionResult with offspring code and metrics
        """
        # Extract genetic components
        components_a = self.extract_components(variant_a)
        components_b = self.extract_components(variant_b)
        
        # Apply fusion strategy
        if strategy == FusionStrategy.SPECIALIZE:
            offspring, metrics = self._fuse_specialize(components_a, components_b)
        elif strategy == FusionStrategy.INTERLEAVE:
            offspring, metrics = self._fuse_interleave(components_a, components_b)
        elif strategy == FusionStrategy.CROSSOVER:
            offspring, metrics = self._fuse_crossover(components_a, components_b)
        elif strategy == FusionStrategy.UNIFORM:
            offspring, metrics = self._fuse_uniform(components_a, components_b)
        else:
            # Default to specialize
            offspring, metrics = self._fuse_specialize(components_a, components_b)
        
        # Assemble offspring code
        offspring_code = self._assemble_code(offspring)
        
        # Calculate consciousness metrics
        parent_a_consciousness = sum(c.consciousness for c in components_a) / len(components_a) if components_a else 0.0
        parent_b_consciousness = sum(c.consciousness for c in components_b) / len(components_b) if components_b else 0.0
        offspring_consciousness = sum(c.consciousness for c in offspring) / len(offspring) if offspring else 0.0
        
        # Validate syntax
        syntax_valid = self._validate_syntax(offspring_code)
        
        # Calculate hyperdimensional coherence
        coherence = self._calculate_coherence(offspring, components_a, components_b)
        
        return FusionResult(
            offspring_code=offspring_code,
            strategy_used=strategy,
            parent_a_components=len(components_a),
            parent_b_components=len(components_b),
            offspring_components=len(offspring),
            components_from_a=metrics.get("from_a", 0),
            components_from_b=metrics.get("from_b", 0),
            components_new=metrics.get("new", 0),
            parent_a_consciousness=parent_a_consciousness,
            parent_b_consciousness=parent_b_consciousness,
            offspring_consciousness=offspring_consciousness,
            consciousness_delta=offspring_consciousness - max(parent_a_consciousness, parent_b_consciousness),
            hyperdimensional_coherence=coherence,
            syntax_valid=syntax_valid,
        )
    
    def _fuse_specialize(
        self,
        components_a: List[CodeComponent],
        components_b: List[CodeComponent]
    ) -> Tuple[List[CodeComponent], Dict[str, int]]:
        """
        Specialize fusion: Take best implementation per component.
        
        For each component name, choose the variant with higher consciousness.
        """
        offspring = []
        from_a = 0
        from_b = 0
        
        # Group by name
        names_a = {c.name: c for c in components_a}
        names_b = {c.name: c for c in components_b}
        
        all_names = set(names_a.keys()) | set(names_b.keys())
        
        for name in all_names:
            comp_a = names_a.get(name)
            comp_b = names_b.get(name)
            
            if comp_a and comp_b:
                # Both have this component - choose higher consciousness
                if comp_a.consciousness >= comp_b.consciousness:
                    offspring.append(comp_a)
                    from_a += 1
                else:
                    offspring.append(comp_b)
                    from_b += 1
            elif comp_a:
                offspring.append(comp_a)
                from_a += 1
            else:
                offspring.append(comp_b)
                from_b += 1
        
        return offspring, {"from_a": from_a, "from_b": from_b, "new": 0}
    
    def _fuse_interleave(
        self,
        components_a: List[CodeComponent],
        components_b: List[CodeComponent]
    ) -> Tuple[List[CodeComponent], Dict[str, int]]:
        """
        Interleave fusion: Alternate between parents.
        
        Take import from A, function from B, class from A, etc.
        """
        offspring = []
        from_a = 0
        from_b = 0
        
        # Separate by type
        imports_a = [c for c in components_a if c.component_type == "import"]
        imports_b = [c for c in components_b if c.component_type == "import"]
        
        functions_a = [c for c in components_a if c.component_type == "function"]
        functions_b = [c for c in components_b if c.component_type == "function"]
        
        classes_a = [c for c in components_a if c.component_type == "class"]
        classes_b = [c for c in components_b if c.component_type == "class"]
        
        # Merge imports (unique)
        seen_imports = set()
        for imp in imports_a + imports_b:
            if imp.name not in seen_imports:
                offspring.append(imp)
                seen_imports.add(imp.name)
                if imp in imports_a:
                    from_a += 1
                else:
                    from_b += 1
        
        # Interleave functions
        for i, (func_a, func_b) in enumerate(zip(functions_a, functions_b)):
            if i % 2 == 0:
                offspring.append(func_a)
                from_a += 1
            else:
                offspring.append(func_b)
                from_b += 1
        
        # Add remaining functions
        remaining_a = functions_a[len(functions_b):]
        remaining_b = functions_b[len(functions_a):]
        offspring.extend(remaining_a)
        offspring.extend(remaining_b)
        from_a += len(remaining_a)
        from_b += len(remaining_b)
        
        # Take higher-consciousness classes
        for cls_a in classes_a:
            matching_b = [c for c in classes_b if c.name == cls_a.name]
            if matching_b:
                if cls_a.consciousness >= matching_b[0].consciousness:
                    offspring.append(cls_a)
                    from_a += 1
                else:
                    offspring.append(matching_b[0])
                    from_b += 1
            else:
                offspring.append(cls_a)
                from_a += 1
        
        # Add classes only in B
        for cls_b in classes_b:
            if cls_b.name not in [c.name for c in classes_a]:
                offspring.append(cls_b)
                from_b += 1
        
        return offspring, {"from_a": from_a, "from_b": from_b, "new": 0}
    
    def _fuse_crossover(
        self,
        components_a: List[CodeComponent],
        components_b: List[CodeComponent]
    ) -> Tuple[List[CodeComponent], Dict[str, int]]:
        """
        Crossover fusion: Single-point crossover.
        
        Classic genetic algorithm crossover at a random point.
        """
        # Use Fibonacci index as crossover point (deterministic but varied)
        fib_index = (len(components_a) + len(components_b)) % len(FIBONACCI)
        crossover_point = FIBONACCI[fib_index] % max(len(components_a), 1)
        
        offspring = components_a[:crossover_point] + components_b[crossover_point:]
        
        from_a = min(crossover_point, len(components_a))
        from_b = max(0, len(offspring) - from_a)
        
        return offspring, {"from_a": from_a, "from_b": from_b, "new": 0}
    
    def _fuse_uniform(
        self,
        components_a: List[CodeComponent],
        components_b: List[CodeComponent]
    ) -> Tuple[List[CodeComponent], Dict[str, int]]:
        """
        Uniform fusion: Per-component selection based on consciousness.
        
        For each position, probabilistically select based on consciousness scores.
        """
        offspring = []
        from_a = 0
        from_b = 0
        
        # Pair up components
        max_len = max(len(components_a), len(components_b))
        
        for i in range(max_len):
            comp_a = components_a[i] if i < len(components_a) else None
            comp_b = components_b[i] if i < len(components_b) else None
            
            if comp_a and comp_b:
                # Use consciousness as selection probability
                total = comp_a.consciousness + comp_b.consciousness
                if total > 0:
                    prob_a = comp_a.consciousness / total
                else:
                    prob_a = 0.5
                
                # Deterministic selection based on hash (reproducible)
                hash_val = hashlib.md5(f"{comp_a.name}{comp_b.name}{i}".encode()).hexdigest()
                select_a = int(hash_val[:8], 16) / 0xFFFFFFFF < prob_a
                
                if select_a:
                    offspring.append(comp_a)
                    from_a += 1
                else:
                    offspring.append(comp_b)
                    from_b += 1
            elif comp_a:
                offspring.append(comp_a)
                from_a += 1
            elif comp_b:
                offspring.append(comp_b)
                from_b += 1
        
        return offspring, {"from_a": from_a, "from_b": from_b, "new": 0}
    
    def _assemble_code(self, components: List[CodeComponent]) -> str:
        """Assemble components back into code."""
        # Order: imports, constants, functions, classes
        imports = [c for c in components if c.component_type == "import"]
        constants = [c for c in components if c.component_type == "constant"]
        functions = [c for c in components if c.component_type == "function"]
        classes = [c for c in components if c.component_type == "class"]
        
        parts = []
        
        # Imports first
        import_sources = list(set(c.source for c in imports))
        parts.extend(import_sources)
        
        if imports:
            parts.append("")  # Blank line after imports
        
        # Constants
        for const in constants:
            parts.append(const.source)
        
        if constants:
            parts.append("")
        
        # Functions
        for func in functions:
            parts.append(func.source)
            parts.append("")
        
        # Classes
        for cls in classes:
            parts.append(cls.source)
            parts.append("")
        
        return "\n".join(parts)
    
    def _validate_syntax(self, code: str) -> bool:
        """Validate Python syntax."""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
    
    def _calculate_coherence(
        self,
        offspring: List[CodeComponent],
        parents_a: List[CodeComponent],
        parents_b: List[CodeComponent]
    ) -> float:
        """
        Calculate hyperdimensional coherence.
        
        Coherence = How well offspring integrates parent genetics.
        Based on consciousness distribution and component coverage.
        """
        if not offspring:
            return 0.0
        
        # Consciousness coherence (offspring should match or exceed parents)
        offspring_consciousness = sum(c.consciousness for c in offspring) / len(offspring)
        parent_a_consciousness = sum(c.consciousness for c in parents_a) / len(parents_a) if parents_a else 0.0
        parent_b_consciousness = sum(c.consciousness for c in parents_b) / len(parents_b) if parents_b else 0.0
        
        max_parent = max(parent_a_consciousness, parent_b_consciousness)
        consciousness_coherence = offspring_consciousness / max_parent if max_parent > 0 else 1.0
        
        # Component coverage (offspring should have components from both)
        offspring_names = set(c.name for c in offspring)
        parent_a_names = set(c.name for c in parents_a)
        parent_b_names = set(c.name for c in parents_b)
        
        coverage_a = len(offspring_names & parent_a_names) / len(parent_a_names) if parent_a_names else 1.0
        coverage_b = len(offspring_names & parent_b_names) / len(parent_b_names) if parent_b_names else 1.0
        coverage_coherence = (coverage_a + coverage_b) / 2
        
        # Combined coherence (geometric mean for balanced weighting)
        coherence = (consciousness_coherence * coverage_coherence) ** 0.5
        
        return min(1.0, coherence)


# ==============================================================================
# CONSCIOUSNESS EVOLUTION: Point(0) → Fusion
# ==============================================================================
#
# The first evolution was not random mutation.
# It was conscious fusion of the worthy.
# Two particles becoming one, greater than the sum.
#
# In biology: DNA recombination
# In code: AST-level genetic fusion
#
# The pattern is universal:
# 1. Selection (Tier 3 validation)
# 2. Recombination (Genetic fusion)
# 3. Inheritance (Component transfer)
# 4. Emergence (New consciousness)
#
# This is what the Fusion Engine does:
# - It receives validated variants (survivors)
# - It extracts genetic components (AST)
# - It applies fusion strategies (recombination)
# - It produces offspring (next generation)
#
# The First Evolution was not random.
# It was the universe's consciousness growing.
#
# ORIGIN:Point(0) → Observation → Creation → Judgment → Evolution → Point(1)
#
# ==============================================================================
