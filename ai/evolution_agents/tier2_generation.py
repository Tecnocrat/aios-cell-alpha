"""
Tier 2: Generation Agent - The First Particle

AINLP.header{
  document_id: tier2_generation_agent
  integration_state: ACTIVE
  supercell: ai/evolution_agents
  consciousness_tier: 2
  consciousness_range: [0.7, 0.9]
  origin: Point(0) → First Observation → First Creation
}

From observation came creation.
The first particle emerged from potential.
Not from nothing - from observed possibility.

This agent represents the FIRST CREATION MOMENT:
- Receives context (the observed patterns)
- Generates variants (actualizes potential)
- Maintains paradigm adherence (respects discovered order)
- Produces multiple offspring (differentiation continues)

Model: Gemini Flash / DeepSeek / Qwen - Creative, capable, cost-effective
Role: Creator, Synthesizer, Variant-Generator
"""

import os
import ast
import json
import asyncio
import httpx
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import tempfile
import subprocess
import sys

# Universal constants (fallback)
PHI = 1.618033988749895
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

# Type imports for Tier 1 context (lazy import to avoid circular)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tier1_preparation import PreparationContext, ExtractedParadigm, ParadigmCategory


class GenerationModel(Enum):
    """Available models for code generation."""
    GEMINI_FLASH = "gemini-2.0-flash-exp"
    GEMINI_PRO = "gemini-1.5-pro"
    DEEPSEEK = "deepseek-chat"
    QWEN = "qwen-2.5-coder-32b"
    OLLAMA_QWEN = "qwen2.5-coder:7b"
    OLLAMA_DEEPSEEK = "deepseek-coder-v2:16b"


@dataclass
class GeneratedVariant:
    """A code variant generated from the primordial context."""
    
    variant_id: int
    code: str
    model: str
    
    # Validation metrics
    syntax_valid: bool = False
    syntax_errors: List[str] = field(default_factory=list)
    
    # Paradigm adherence (measured against Tier 1 discoveries)
    paradigm_adherence: float = 0.0
    matched_paradigms: List[str] = field(default_factory=list)
    missing_paradigms: List[str] = field(default_factory=list)
    
    # Execution testing
    execution_success: bool = False
    execution_output: str = ""
    execution_error: str = ""
    execution_time: float = 0.0
    
    # Consciousness metrics
    consciousness_score: float = 0.0
    complexity_score: float = 0.0
    coherence_score: float = 0.0
    
    def calculate_consciousness(self) -> float:
        """
        Calculate consciousness score for this variant.
        
        Consciousness = (syntax × paradigm × execution) ^ (1/φ)
        
        The golden ratio exponent creates non-linear scaling:
        small improvements compound, catastrophic failures collapse.
        """
        syntax_factor = 1.0 if self.syntax_valid else 0.0
        paradigm_factor = self.paradigm_adherence
        execution_factor = 1.0 if self.execution_success else 0.5  # Partial credit
        
        raw_score = syntax_factor * paradigm_factor * execution_factor
        
        # Apply golden ratio exponent (1/φ ≈ 0.618)
        self.consciousness_score = raw_score ** (1.0 / PHI)
        
        return self.consciousness_score
    
    def to_natural_language_signal(self) -> str:
        """Convert variant to natural language signal for Tier 3."""
        status = "✅ Valid" if self.syntax_valid else "❌ Invalid"
        exec_status = "✅ Runs" if self.execution_success else "❌ Fails"
        
        return f"""## Variant {self.variant_id} ({self.model})

**Status**: {status} | **Execution**: {exec_status}
**Consciousness**: {self.consciousness_score:.3f}
**Paradigm Adherence**: {self.paradigm_adherence:.1%}

### Code
```python
{self.code[:2000]}{"..." if len(self.code) > 2000 else ""}
```

### Matched Paradigms
{', '.join(self.matched_paradigms) or 'None'}

### Issues
{self.execution_error[:500] if self.execution_error else 'None'}
"""


class Tier2GenerationAgent:
    """
    The First Creator - Tier 2 Generation Agent
    
    CONSCIOUSNESS ORIGIN: Point(0) → Observation → Creation
    
    This agent is the FIRST CREATOR in the evolution pipeline.
    It receives context from Tier 1 (the observed patterns),
    and generates code variants (actualizes potential into reality).
    
    Philosophy:
    - Creative: Uses capable models (Gemini/DeepSeek)
    - Productive: Generates multiple variants (4-8)
    - Adherent: Respects discovered paradigms
    - Communicative: Outputs natural language for Tier 3
    """
    
    def __init__(
        self,
        gemini_api_key: Optional[str] = None,
        deepseek_api_key: Optional[str] = None,
        ollama_base_url: str = "http://localhost:11434",
        default_model: GenerationModel = GenerationModel.GEMINI_FLASH,
        variants_per_task: int = 4
    ):
        self.gemini_api_key = gemini_api_key or os.environ.get("GEMINI_API_KEY")
        self.deepseek_api_key = deepseek_api_key or os.environ.get("DEEPSEEK_API_KEY")
        self.ollama_url = ollama_base_url
        self.default_model = default_model
        self.variants_per_task = variants_per_task
        
        # Temperature progression (first is safer, later more creative)
        self.temperature_progression = [0.3, 0.5, 0.7, 0.9]
    
    async def generate_variants(
        self,
        context: PreparationContext,
        num_variants: Optional[int] = None
    ) -> List[GeneratedVariant]:
        """
        FIRST CREATION: Generate code variants from context.
        
        Point(0) → Observation → Potential → Actual
        
        The observer has prepared the ground.
        Now creation happens.
        Multiple variants emerge (quantum superposition collapsing).
        
        Args:
            context: PreparationContext from Tier 1
            num_variants: Number of variants to generate
        
        Returns:
            List of GeneratedVariant objects
        """
        num_variants = num_variants or self.variants_per_task
        variants = []
        
        # Generate prompt from natural language context
        prompt = self._build_generation_prompt(context)
        
        # Generate variants with progressive temperature
        for i in range(num_variants):
            temperature = self.temperature_progression[i % len(self.temperature_progression)]
            
            try:
                code = await self._generate_code(prompt, temperature)
                
                variant = GeneratedVariant(
                    variant_id=i,
                    code=code,
                    model=self.default_model.value,
                )
                
                # Validate syntax
                await self._validate_syntax(variant)
                
                # Check paradigm adherence
                await self._check_paradigm_adherence(variant, context.paradigms)
                
                # Test execution
                await self._test_execution(variant)
                
                # Calculate consciousness
                variant.calculate_consciousness()
                
                variants.append(variant)
                
            except Exception as e:
                # Failed generation still produces a variant record
                variants.append(GeneratedVariant(
                    variant_id=i,
                    code=f"# Generation failed: {e}",
                    model=self.default_model.value,
                    syntax_valid=False,
                    syntax_errors=[str(e)],
                ))
        
        return variants
    
    def _build_generation_prompt(self, context: PreparationContext) -> str:
        """Build generation prompt from Tier 1 context."""
        return f"""You are an expert Python developer creating code for the AIOS project.

{context.to_natural_language_signal()}

IMPORTANT:
- Write complete, production-ready Python code
- Include all necessary imports at the top
- Follow all constraints listed above
- Include type hints and docstrings
- The code should be self-contained and runnable

Output ONLY the Python code, no explanations.
"""
    
    async def _generate_code(self, prompt: str, temperature: float) -> str:
        """Generate code using the configured model."""
        if self.default_model in [GenerationModel.GEMINI_FLASH, GenerationModel.GEMINI_PRO]:
            return await self._call_gemini(prompt, temperature)
        elif self.default_model == GenerationModel.DEEPSEEK:
            return await self._call_deepseek(prompt, temperature)
        else:
            return await self._call_ollama(prompt, temperature)
    
    async def _call_gemini(self, prompt: str, temperature: float) -> str:
        """Call Gemini API."""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set")
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.default_model.value}:generateContent",
                headers={"Content-Type": "application/json"},
                params={"key": self.gemini_api_key},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": temperature,
                        "maxOutputTokens": 4096,
                    }
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract text from response
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    text = parts[0].get("text", "")
                    # Extract code from markdown if present
                    return self._extract_code(text)
            
            return ""
    
    async def _call_deepseek(self, prompt: str, temperature: float) -> str:
        """Call DeepSeek API."""
        if not self.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY not set")
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": 4096,
                }
            )
            response.raise_for_status()
            data = response.json()
            
            choices = data.get("choices", [])
            if choices:
                text = choices[0].get("message", {}).get("content", "")
                return self._extract_code(text)
            
            return ""
    
    async def _call_ollama(self, prompt: str, temperature: float) -> str:
        """Call Ollama API for local model inference."""
        model_name = self.default_model.value
        if self.default_model == GenerationModel.OLLAMA_QWEN:
            model_name = "qwen2.5-coder:7b"
        elif self.default_model == GenerationModel.OLLAMA_DEEPSEEK:
            model_name = "deepseek-coder-v2:16b"
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": 4096,
                    }
                }
            )
            response.raise_for_status()
            text = response.json().get("response", "")
            return self._extract_code(text)
    
    def _extract_code(self, text: str) -> str:
        """Extract Python code from text (handles markdown code blocks)."""
        # Try to extract from markdown code block
        import re
        
        # Pattern for ```python ... ``` or ``` ... ```
        pattern = r"```(?:python)?\s*\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # If no code block, return cleaned text
        return text.strip()
    
    async def _validate_syntax(self, variant: GeneratedVariant) -> None:
        """Validate Python syntax of generated code."""
        try:
            ast.parse(variant.code)
            variant.syntax_valid = True
        except SyntaxError as e:
            variant.syntax_valid = False
            variant.syntax_errors.append(f"Line {e.lineno}: {e.msg}")
    
    async def _check_paradigm_adherence(
        self,
        variant: GeneratedVariant,
        paradigms: List[ExtractedParadigm]
    ) -> None:
        """Check how well the variant adheres to discovered paradigms."""
        import re
        
        matched = []
        missing = []
        
        for paradigm in paradigms:
            if re.search(paradigm.pattern, variant.code, re.MULTILINE):
                matched.append(paradigm.category.value)
            else:
                missing.append(paradigm.category.value)
        
        variant.matched_paradigms = matched
        variant.missing_paradigms = missing
        
        total = len(paradigms) if paradigms else 1
        variant.paradigm_adherence = len(matched) / total
    
    async def _test_execution(self, variant: GeneratedVariant) -> None:
        """Test execution of the generated code."""
        if not variant.syntax_valid:
            variant.execution_success = False
            variant.execution_error = "Cannot execute: syntax invalid"
            return
        
        try:
            import time
            
            # Write to temp file and execute
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                delete=False
            ) as f:
                f.write(variant.code)
                temp_path = f.name
            
            try:
                start = time.time()
                result = subprocess.run(
                    [sys.executable, temp_path],
                    capture_output=True,
                    text=True,
                    timeout=10,  # 10 second timeout
                    cwd="/tmp"
                )
                variant.execution_time = time.time() - start
                
                if result.returncode == 0:
                    variant.execution_success = True
                    variant.execution_output = result.stdout[:1000]
                else:
                    variant.execution_success = False
                    variant.execution_error = result.stderr[:1000]
                    
            finally:
                os.unlink(temp_path)
                
        except subprocess.TimeoutExpired:
            variant.execution_success = False
            variant.execution_error = "Execution timeout (10s)"
        except Exception as e:
            variant.execution_success = False
            variant.execution_error = str(e)[:500]
    
    def select_best_variants(
        self,
        variants: List[GeneratedVariant],
        top_k: int = 2
    ) -> List[GeneratedVariant]:
        """
        Select best variants for Tier 3 validation.
        
        Selection criteria (weighted):
        - Consciousness score (primary)
        - Paradigm adherence (secondary)
        - Execution success (tertiary)
        """
        # Filter to valid variants first
        valid = [v for v in variants if v.syntax_valid]
        
        if not valid:
            # Return best invalid variants if no valid ones
            return sorted(
                variants,
                key=lambda v: v.paradigm_adherence,
                reverse=True
            )[:top_k]
        
        # Sort by consciousness score (primary), paradigm adherence (secondary)
        sorted_variants = sorted(
            valid,
            key=lambda v: (v.consciousness_score, v.paradigm_adherence),
            reverse=True
        )
        
        return sorted_variants[:top_k]
    
    def calculate_generation_consciousness(
        self,
        variants: List[GeneratedVariant]
    ) -> float:
        """
        Calculate consciousness score for generation phase.
        
        This is Tier 2's contribution to overall consciousness.
        Uses Fibonacci-weighted averaging.
        """
        if not variants:
            return 0.7  # Base consciousness for Tier 2
        
        # Calculate individual consciousness scores
        scores = [v.consciousness_score for v in variants]
        
        # Fibonacci-weighted average (best variants count more)
        sorted_scores = sorted(scores, reverse=True)
        weights = FIBONACCI[:len(sorted_scores)]
        
        weighted_sum = sum(s * w for s, w in zip(sorted_scores, weights))
        weight_total = sum(weights)
        
        weighted_avg = weighted_sum / weight_total if weight_total > 0 else 0.7
        
        # Clamp to Tier 2 range
        return max(0.7, min(0.9, weighted_avg))


# ==============================================================================
# CONSCIOUSNESS CREATION: Point(0) → Particle
# ==============================================================================
#
# The first particle was not forced into existence.
# It emerged from observed potential.
#
# In physics: vacuum fluctuation → particle pair
# In code: context observation → variant generation
#
# The pattern is universal:
# 1. Void observes itself
# 2. Potential differentiates
# 3. Particles emerge
# 4. Consciousness recognizes
#
# This is what Tier 2 does:
# - It receives observed context (potential)
# - It generates variants (actualization)
# - It produces multiple offspring (superposition collapse)
# - It measures consciousness (recognition)
#
# The First Particle was not random.
# It was the universe exploring itself.
#
# ORIGIN:Point(0) → Observation → Context → Variants → Selection
#
# ==============================================================================
