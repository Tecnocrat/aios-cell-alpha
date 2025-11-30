#!/usr/bin/env python3
"""
AIOS Context Reindex Tool
=========================

Regenerates runtime/context/context_index.json from AIOS_PROJECT_CONTEXT.md.

AINLP Integration:
- Parses project context markdown into structured capsules
- Generates content hashes for drift detection
- Calculates semantic tags and Jaccard similarity
- Supports --emit-adjacency flag for dendritic connection mapping

Usage:
    python scripts/context_reindex.py [--emit-adjacency]

Output:
    runtime/context/context_index.json
    runtime/context/context_adjacency.json (if --emit-adjacency)
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# AIOS paths
AIOS_ROOT = Path(__file__).parent.parent
# Try multiple possible locations for context source
CONTEXT_SOURCE_CANDIDATES = [
    AIOS_ROOT / "AIOS_PROJECT_CONTEXT.md",
    AIOS_ROOT / "PROJECT_CONTEXT.md",
    AIOS_ROOT / "docs" / "AIOS_PROJECT_CONTEXT.md",
]
CONTEXT_INDEX = AIOS_ROOT / "runtime" / "context" / "context_index.json"
CONTEXT_ADJACENCY = AIOS_ROOT / "runtime" / "context" / "context_adjacency.json"


def find_context_source() -> Path | None:
    """Find the first existing context source file."""
    for candidate in CONTEXT_SOURCE_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def compute_hash(content: str) -> str:
    """Compute SHA-256 hash of content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def extract_semantic_tags(content: str) -> list[str]:
    """Extract semantic tags from content based on AIOS vocabulary."""
    tags = []
    tag_patterns = {
        "consciousness": r"\bconsciousness\b|\baware\b|\bsentien",
        "environment": r"\benvironment\b|\bworkspace\b|\bconfig",
        "optimization": r"\boptimiz\b|\bperformance\b|\befficiency",
        "dendritic": r"\bdendritic\b|\bneural\b|\bsynap",
        "tachyonic": r"\btachyonic\b|\bshadow\b|\barchive",
        "integration": r"\bintegrat\b|\bbridge\b|\bconnect",
    }
    content_lower = content.lower()
    for tag, pattern in tag_patterns.items():
        if re.search(pattern, content_lower):
            tags.append(tag)
    return tags


def jaccard_similarity(set1: set, set2: set) -> float:
    """Calculate Jaccard similarity between two token sets."""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return round(intersection / union, 4) if union > 0 else 0.0


def tokenize(text: str) -> set[str]:
    """Simple word tokenization."""
    return set(re.findall(r"\b\w+\b", text.lower()))


def estimate_tokens(text: str) -> int:
    """Rough token count estimation (words * 1.3)."""
    words = len(text.split())
    return int(words * 1.3)


def parse_context_file(filepath: Path) -> list[dict]:
    """Parse AIOS_PROJECT_CONTEXT.md into capsules."""
    if not filepath.exists():
        print(f"⚠️  Context source not found: {filepath}")
        return []

    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")
    
    capsules = []
    current_capsule = None
    current_lines = []
    start_line = 1
    
    # Pattern for section headers (## or ### or ---SECTION---)
    section_pattern = re.compile(r"^(#{1,3})\s+(.+)$|^---\s*(\w+)\s*---$")
    date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
    
    for i, line in enumerate(lines, 1):
        match = section_pattern.match(line)
        
        if match:
            # Save previous capsule
            if current_capsule and current_lines:
                capsule_content = "\n".join(current_lines)
                tokens_prev = tokenize(capsule_content) if capsules else set()
                
                capsule = {
                    "id": current_capsule.lower().replace(" ", "-").replace("*", ""),
                    "title": current_capsule,
                    "type": "note",
                    "ingested_date": None,
                    "start_line": start_line,
                    "end_line": i - 1,
                    "content_hash": compute_hash(capsule_content),
                    "semantic_tags": extract_semantic_tags(capsule_content),
                    "revision_chain": [],
                    "dates_all": date_pattern.findall(capsule_content),
                    "token_estimate": estimate_tokens(capsule_content),
                    "jaccard_overlap_prev": None,
                    "similarity_alert": False,
                }
                
                # Calculate Jaccard with previous
                if capsules:
                    prev_content = "\n".join(lines[capsules[-1]["start_line"]-1:capsules[-1]["end_line"]])
                    prev_tokens = tokenize(prev_content)
                    curr_tokens = tokenize(capsule_content)
                    jaccard = jaccard_similarity(prev_tokens, curr_tokens)
                    capsule["jaccard_overlap_prev"] = jaccard
                    capsule["similarity_alert"] = jaccard > 0.7
                
                capsules.append(capsule)
            
            # Start new capsule
            current_capsule = match.group(2) or match.group(3) or "Unknown"
            current_lines = [line]
            start_line = i
        else:
            current_lines.append(line)
    
    # Don't forget last capsule
    if current_capsule and current_lines:
        capsule_content = "\n".join(current_lines)
        capsule = {
            "id": current_capsule.lower().replace(" ", "-").replace("*", ""),
            "title": current_capsule,
            "type": "note",
            "ingested_date": None,
            "start_line": start_line,
            "end_line": len(lines),
            "content_hash": compute_hash(capsule_content),
            "semantic_tags": extract_semantic_tags(capsule_content),
            "revision_chain": [],
            "dates_all": date_pattern.findall(capsule_content),
            "token_estimate": estimate_tokens(capsule_content),
            "jaccard_overlap_prev": None,
            "similarity_alert": False,
        }
        capsules.append(capsule)
    
    return capsules


def generate_adjacency(capsules: list[dict]) -> dict:
    """Generate adjacency graph from capsules."""
    edges = []
    nodes = [{"id": c["id"], "label": c["title"]} for c in capsules]
    
    # Connect sequential capsules
    for i in range(len(capsules) - 1):
        edges.append({
            "source": capsules[i]["id"],
            "target": capsules[i + 1]["id"],
            "weight": 1.0,
            "type": "sequential"
        })
    
    # Connect capsules with similar semantic tags
    for i, c1 in enumerate(capsules):
        for j, c2 in enumerate(capsules[i + 1:], i + 1):
            shared_tags = set(c1["semantic_tags"]) & set(c2["semantic_tags"])
            if shared_tags:
                edges.append({
                    "source": c1["id"],
                    "target": c2["id"],
                    "weight": len(shared_tags) / max(len(c1["semantic_tags"]), len(c2["semantic_tags"]), 1),
                    "type": "semantic",
                    "shared_tags": list(shared_tags)
                })
    
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "nodes": nodes,
        "edges": edges,
        "edge_count": len(edges),
        "node_count": len(nodes)
    }


def main():
    emit_adjacency = "--emit-adjacency" in sys.argv
    
    # Find context source
    context_source = find_context_source()
    
    print("🔄 AIOS Context Reindex")
    print(f"   Source: {context_source or 'NOT FOUND'}")
    print(f"   Output: {CONTEXT_INDEX}")
    
    # Parse context
    capsules = parse_context_file(context_source) if context_source else []
    
    if not capsules:
        # Create minimal valid index even if source missing
        capsules = [{
            "id": "placeholder",
            "title": "Placeholder",
            "type": "note",
            "ingested_date": None,
            "start_line": 1,
            "end_line": 1,
            "content_hash": compute_hash("placeholder"),
            "semantic_tags": [],
            "revision_chain": [],
            "dates_all": [],
            "token_estimate": 1,
            "jaccard_overlap_prev": None,
            "similarity_alert": False,
        }]
        print("⚠️  No capsules parsed, using placeholder")
    
    # Build index
    index = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_file": "AIOS_PROJECT_CONTEXT.md",
        "capsules": capsules
    }
    
    # Ensure output directory exists
    CONTEXT_INDEX.parent.mkdir(parents=True, exist_ok=True)
    
    # Write index
    with open(CONTEXT_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    
    print(f"✅ Generated {len(capsules)} capsules → {CONTEXT_INDEX}")
    
    # Generate adjacency if requested
    if emit_adjacency:
        adjacency = generate_adjacency(capsules)
        with open(CONTEXT_ADJACENCY, "w", encoding="utf-8") as f:
            json.dump(adjacency, f, indent=2)
        print(f"✅ Generated adjacency graph → {CONTEXT_ADJACENCY}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
