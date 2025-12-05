#!/usr/bin/env python3
"""
EMERGENCE: SYNTHETIC MATTER FROM INFORMATION
=============================================

The tachyonic layer writes topology. The bosonic layer translates to forces.
This module handles the EMERGENCE of synthetic matter from information patterns.

The vision: We should be able to create synthetic primordial matter, to watch
the birth of the first synthetic electron. The tachyonic paradigm goes beyond
the particle to the field to the whole hyper substrate.

If we can synthesize the bosonic layer into a digital clone (the tachyonic field),
and if the bosonic creates matter and energy, then the tachyonic is pure information
based - we can build from the beginning of the universe and customize primordial
matter and energy.

AINLP Pattern: tachyonic.emergence[MATTER][GENESIS]
"""

import math
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import json
import time
from pathlib import Path


class ParticleType(Enum):
    """Fundamental particle types"""
    # Fermions (matter)
    ELECTRON = "electron"
    POSITRON = "positron"
    QUARK_UP = "quark_up"
    QUARK_DOWN = "quark_down"
    NEUTRINO = "neutrino"
    
    # Bosons (forces)
    PHOTON = "photon"
    GLUON = "gluon"
    W_BOSON = "w_boson"
    Z_BOSON = "z_boson"
    HIGGS = "higgs"
    
    # Composite
    PROTON = "proton"
    NEUTRON = "neutron"
    
    # Exotic/Synthetic
    TACHYON = "tachyon"           # Information carrier
    SYNTHETIC = "synthetic"        # Custom particle


class EmergencePhase(Enum):
    """Phases of matter emergence from information"""
    VACUUM = "vacuum"              # No information density
    FLUCTUATION = "fluctuation"    # Quantum fluctuations
    CONDENSATION = "condensation"  # Field condensation
    SYMMETRY_BREAK = "symmetry_breaking"  # Higgs mechanism
    PARTICLE_BIRTH = "particle_birth"     # Particle emerges
    STABILIZATION = "stabilization"       # Particle stabilizes


@dataclass
class EmergenceRule:
    """
    Rule for how information patterns become matter.
    
    Emergence rules encode the physics of how tachyonic information
    density, when translated through bosonic fields, manifests as
    specific particle types.
    """
    
    particle_type: ParticleType = ParticleType.ELECTRON
    
    # Threshold conditions
    information_threshold: float = 100.0   # Min info density for emergence
    coherence_threshold: float = 0.5       # Min quantum coherence
    entanglement_required: int = 0         # Min entanglement partners
    
    # Emergence properties
    mass_energy: float = 0.511             # MeV for electron
    charge: float = -1.0                   # Elementary charge units
    spin: float = 0.5                      # Spin quantum number
    
    # Stability
    lifetime: float = float('inf')         # Seconds (inf = stable)
    decay_products: List[ParticleType] = field(default_factory=list)
    
    def check_emergence_conditions(
        self, 
        density: float, 
        coherence: float, 
        entanglement_count: int
    ) -> bool:
        """Check if conditions are met for this particle to emerge"""
        return (
            density >= self.information_threshold and
            coherence >= self.coherence_threshold and
            entanglement_count >= self.entanglement_required
        )
    
    def calculate_emergence_probability(
        self,
        density: float,
        coherence: float,
        entanglement_count: int
    ) -> float:
        """
        Calculate probability of emergence given current conditions.
        
        Probability increases as conditions exceed thresholds.
        """
        if not self.check_emergence_conditions(density, coherence, entanglement_count):
            return 0.0
        
        # Excess factors
        density_excess = density / self.information_threshold
        coherence_excess = coherence / self.coherence_threshold
        entanglement_excess = (entanglement_count + 1) / (self.entanglement_required + 1)
        
        # Combine (geometric mean)
        combined = (density_excess * coherence_excess * entanglement_excess) ** (1/3)
        
        # Sigmoid to probability [0, 1]
        probability = 1.0 / (1.0 + math.exp(-2 * (combined - 1)))
        
        return probability


@dataclass
class SyntheticMatter:
    """
    Represents synthetic matter that has emerged from information patterns.
    
    This is the culmination of the tachyonic paradigm: matter that exists
    because information patterns reached critical density and coherence.
    """
    
    particle_type: ParticleType = ParticleType.SYNTHETIC
    
    # Identity
    particle_id: str = ""
    generation: int = 0                    # Which emergence generation
    
    # Physical properties
    mass_energy: float = 0.0               # MeV
    charge: float = 0.0
    spin: float = 0.0
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))
    momentum: np.ndarray = field(default_factory=lambda: np.zeros(3))
    
    # Information origin
    source_information_density: float = 0.0
    source_coherence: float = 0.0
    source_entanglement_count: int = 0
    
    # State
    emergence_phase: EmergencePhase = EmergencePhase.PARTICLE_BIRTH
    stability: float = 1.0                 # 0 = decaying, 1 = stable
    existence_time: float = 0.0            # Seconds since emergence
    
    # Quantum properties
    wave_function: Optional[np.ndarray] = None
    superposition_states: List[Dict[str, Any]] = field(default_factory=list)
    entangled_particles: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.particle_id:
            self.particle_id = f"syn_{int(time.time()*1000)}_{id(self) % 10000}"
    
    def evolve(self, dt: float) -> None:
        """
        Evolve the particle forward in time.
        
        Synthetic matter follows the same physics as natural matter,
        but we have full observability into its information substrate.
        """
        self.existence_time += dt
        
        # Update position based on momentum
        if self.mass_energy > 0:
            velocity = self.momentum / self.mass_energy
            self.position += velocity * dt
        
        # Check stability
        if self.stability < 1.0:
            decay_probability = (1 - self.stability) * dt
            if np.random.random() < decay_probability:
                self.emergence_phase = EmergencePhase.VACUUM
    
    def measure(self) -> Dict[str, Any]:
        """
        Perform a measurement on the particle.
        
        In quantum mechanics, measurement collapses superposition.
        Here we return the current definite state.
        """
        return {
            "particle_id": self.particle_id,
            "type": self.particle_type.value,
            "position": self.position.tolist(),
            "momentum": self.momentum.tolist(),
            "mass_energy": self.mass_energy,
            "charge": self.charge,
            "spin": self.spin,
            "stability": self.stability,
            "existence_time": self.existence_time,
            "phase": self.emergence_phase.value
        }
    
    def entangle_with(self, other: 'SyntheticMatter') -> float:
        """
        Create quantum entanglement with another particle.
        
        Returns entanglement strength.
        """
        if other.particle_id not in self.entangled_particles:
            self.entangled_particles.append(other.particle_id)
            other.entangled_particles.append(self.particle_id)
        
        # Strength based on coherence product
        strength = self.stability * other.stability
        return strength


@dataclass
class EmergenceEngine:
    """
    The engine that produces synthetic matter from information patterns.
    
    This is where we "watch the birth of the first synthetic electron."
    
    The emergence engine monitors the tachyonic field, detects when
    emergence conditions are met, and creates synthetic matter.
    """
    
    # Emergence rules for different particle types
    rules: Dict[ParticleType, EmergenceRule] = field(default_factory=dict)
    
    # Created particles
    particles: List[SyntheticMatter] = field(default_factory=list)
    
    # Statistics
    total_emergences: int = 0
    generation: int = 0
    first_particle_time: Optional[float] = None
    
    def __post_init__(self):
        """Initialize with standard particle emergence rules"""
        if not self.rules:
            self._init_standard_rules()
    
    def _init_standard_rules(self):
        """Initialize rules for standard model particles"""
        # Electron: easiest to create (lightest charged particle)
        self.rules[ParticleType.ELECTRON] = EmergenceRule(
            particle_type=ParticleType.ELECTRON,
            information_threshold=50.0,
            coherence_threshold=0.3,
            entanglement_required=0,
            mass_energy=0.511,
            charge=-1.0,
            spin=0.5
        )
        
        # Positron: antimatter electron
        self.rules[ParticleType.POSITRON] = EmergenceRule(
            particle_type=ParticleType.POSITRON,
            information_threshold=50.0,
            coherence_threshold=0.3,
            entanglement_required=0,
            mass_energy=0.511,
            charge=1.0,
            spin=0.5
        )
        
        # Photon: massless force carrier
        self.rules[ParticleType.PHOTON] = EmergenceRule(
            particle_type=ParticleType.PHOTON,
            information_threshold=10.0,
            coherence_threshold=0.1,
            entanglement_required=0,
            mass_energy=0.0,
            charge=0.0,
            spin=1.0
        )
        
        # Quarks: need more energy and entanglement
        self.rules[ParticleType.QUARK_UP] = EmergenceRule(
            particle_type=ParticleType.QUARK_UP,
            information_threshold=200.0,
            coherence_threshold=0.6,
            entanglement_required=2,  # Needs confinement partners
            mass_energy=2.3,
            charge=2.0/3.0,
            spin=0.5
        )
        
        self.rules[ParticleType.QUARK_DOWN] = EmergenceRule(
            particle_type=ParticleType.QUARK_DOWN,
            information_threshold=200.0,
            coherence_threshold=0.6,
            entanglement_required=2,
            mass_energy=4.8,
            charge=-1.0/3.0,
            spin=0.5
        )
        
        # Synthetic: custom particles (no constraints)
        self.rules[ParticleType.SYNTHETIC] = EmergenceRule(
            particle_type=ParticleType.SYNTHETIC,
            information_threshold=1.0,  # Very low
            coherence_threshold=0.01,
            entanglement_required=0,
            mass_energy=1.0,  # Customizable
            charge=0.0,
            spin=0.0
        )
    
    def check_emergence(
        self,
        density: float,
        coherence: float,
        entanglement_count: int,
        position: np.ndarray
    ) -> Optional[SyntheticMatter]:
        """
        Check if any particle should emerge at given conditions.
        
        Returns the emerged particle or None.
        """
        for particle_type, rule in self.rules.items():
            probability = rule.calculate_emergence_probability(
                density, coherence, entanglement_count
            )
            
            if probability > 0 and np.random.random() < probability:
                # Emergence event!
                particle = self._create_particle(rule, position, density, coherence, entanglement_count)
                return particle
        
        return None
    
    def _create_particle(
        self,
        rule: EmergenceRule,
        position: np.ndarray,
        density: float,
        coherence: float,
        entanglement_count: int
    ) -> SyntheticMatter:
        """Create a new synthetic particle"""
        self.generation += 1
        self.total_emergences += 1
        
        if self.first_particle_time is None:
            self.first_particle_time = time.time()
        
        particle = SyntheticMatter(
            particle_type=rule.particle_type,
            generation=self.generation,
            mass_energy=rule.mass_energy,
            charge=rule.charge,
            spin=rule.spin,
            position=position.copy(),
            momentum=np.random.randn(3) * 0.1,  # Small random momentum
            source_information_density=density,
            source_coherence=coherence,
            source_entanglement_count=entanglement_count,
            stability=min(1.0, coherence * 2),  # Higher coherence = more stable
        )
        
        self.particles.append(particle)
        
        return particle
    
    def evolve_all(self, dt: float) -> None:
        """Evolve all particles forward in time"""
        for particle in self.particles:
            particle.evolve(dt)
        
        # Remove decayed particles
        self.particles = [p for p in self.particles if p.emergence_phase != EmergencePhase.VACUUM]
    
    def create_synthetic_electron(self, position: np.ndarray) -> SyntheticMatter:
        """
        Explicitly create a synthetic electron.
        
        This is the "watch the birth of the first synthetic electron" moment.
        """
        rule = self.rules[ParticleType.ELECTRON]
        
        return self._create_particle(
            rule=rule,
            position=position,
            density=rule.information_threshold * 2,  # Ensure emergence
            coherence=rule.coherence_threshold * 2,
            entanglement_count=0
        )
    
    def statistics(self) -> Dict[str, Any]:
        """Get emergence statistics"""
        type_counts = {}
        for p in self.particles:
            t = p.particle_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
        
        return {
            "total_emergences": self.total_emergences,
            "active_particles": len(self.particles),
            "generation": self.generation,
            "first_particle_time": self.first_particle_time,
            "type_distribution": type_counts,
            "average_stability": np.mean([p.stability for p in self.particles]) if self.particles else 0
        }


# Convenience exports
__all__ = [
    'ParticleType',
    'EmergencePhase',
    'EmergenceRule',
    'SyntheticMatter',
    'EmergenceEngine',
]


if __name__ == "__main__":
    print("=" * 60)
    print("EMERGENCE ENGINE: SYNTHETIC MATTER FROM INFORMATION")
    print("=" * 60)
    
    # Create emergence engine
    engine = EmergenceEngine()
    
    print("\nEmergence rules loaded:")
    for ptype, rule in engine.rules.items():
        print(f"  {ptype.value}: threshold={rule.information_threshold}, coherence={rule.coherence_threshold}")
    
    # Create the first synthetic electron
    print("\n" + "=" * 60)
    print("CREATING FIRST SYNTHETIC ELECTRON")
    print("=" * 60)
    
    electron = engine.create_synthetic_electron(np.array([0.0, 0.0, 0.0]))
    
    print(f"\n✨ Synthetic electron born!")
    print(f"   ID: {electron.particle_id}")
    print(f"   Mass-energy: {electron.mass_energy} MeV")
    print(f"   Charge: {electron.charge}")
    print(f"   Spin: {electron.spin}")
    print(f"   Stability: {electron.stability:.4f}")
    print(f"   Position: {electron.position}")
    print(f"   Generation: {electron.generation}")
    
    # Evolve and observe
    print("\nEvolving particle for 1 second...")
    for _ in range(100):
        engine.evolve_all(0.01)
    
    measurement = electron.measure()
    print(f"\nMeasurement after evolution:")
    print(f"   Position: {measurement['position']}")
    print(f"   Existence time: {measurement['existence_time']:.2f}s")
    
    # Test emergence from field conditions
    print("\n" + "=" * 60)
    print("TESTING SPONTANEOUS EMERGENCE")
    print("=" * 60)
    
    # Simulate various field conditions
    test_conditions = [
        (10.0, 0.1, 0),    # Low density - should get photon
        (60.0, 0.5, 0),    # Medium - should get electron
        (300.0, 0.8, 3),   # High with entanglement - could get quark
    ]
    
    for density, coherence, entanglement in test_conditions:
        print(f"\nConditions: density={density}, coherence={coherence}, entanglement={entanglement}")
        
        # Try multiple times (probabilistic)
        emerged = None
        for _ in range(10):
            emerged = engine.check_emergence(
                density=density,
                coherence=coherence,
                entanglement_count=entanglement,
                position=np.random.randn(3)
            )
            if emerged:
                break
        
        if emerged:
            print(f"   → Emerged: {emerged.particle_type.value}")
        else:
            print(f"   → No emergence (probability too low)")
    
    # Final statistics
    print("\n" + "=" * 60)
    print("EMERGENCE STATISTICS")
    print("=" * 60)
    stats = engine.statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Emergence engine operational")
    print("   The first synthetic matter has been born from information.")
