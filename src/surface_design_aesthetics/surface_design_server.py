"""
Surface Design Aesthetics MCP Server
======================================

Visual aesthetics derived from material science and surface treatment design.

Covers the full range of surface treatments from mirror-smooth automotive lacquer
to densely spiked organic seedcoats. Parametrizes specularity, micro-texture,
material hardness, organic/synthetic character, and pattern scale.

Phase 2.6: Rhythmic presets with 5 curated oscillation patterns
    - sheen_oscillation (15): matte ↔ mirror
    - texture_accretion (19): smooth ↔ spiky (prime period)
    - material_softening (21): stone ↔ woven
    - nature_synthesis (24): synthetic ↔ organic
    - full_palette_morph (30): glass ↔ textile (LCM hub)

Phase 2.7: Attractor visualization prompt generation
    - 7 discovered/curated attractor presets from Tier 4D analysis
    - Composite, split-view, and sequence prompt modes
    - Domain registry helper for emergent attractor discovery

Layer Architecture:
    Layer 1 (Taxonomy):     Pure lookup, 0 tokens
    Layer 2 (Deterministic): Parameter mapping, distance, trajectory,
                             rhythm, vocabulary, attractor prompts — 0 tokens
    Layer 3 (Synthesis):     Claude-assisted visualization context — ~100-200 tokens

Compatible with:
    - aesthetic-dynamics-core: Trajectory integration, attractor discovery
    - catastrophe-morph-mcp: Cross-domain composition (material ↔ geometry)
    - diatom-morph-mcp: Microscopic surface structure overlay
    - composition-graph-mcp: Central orchestrator for multi-domain composition

Deployment:
    fastmcp run surface_design_server.py
    # or
    fastmcp deploy surface_design_server.py --name surface-design-aesthetics
"""

import json
import math
import re
from typing import Dict, List, Optional, Any
from fastmcp import FastMCP

# ============================================================================
# Server Initialization
# ============================================================================

mcp = FastMCP("surface_design_mcp")

# ============================================================================
# Constants: Parameter Space Definition
# ============================================================================

PARAMETER_NAMES = [
    "specularity",           # 0 = fully matte/absorbent → 1 = perfect mirror
    "micro_texture_density", # 0 = glass-smooth → 1 = densely packed micro-features
    "material_hardness",     # 0 = soft/pliable/draped → 1 = rigid/crystalline/brittle
    "organic_synthetic_ratio",  # 0 = purely manufactured → 1 = purely biological/natural
    "surface_pattern_scale", # 0 = no pattern/uniform → 1 = large macro-repeat pattern
]

PARAMETER_BOUNDS = [0.0, 1.0]
DIMENSIONALITY = 5

# ============================================================================
# Constants: 9 Canonical States
# ============================================================================

CANONICAL_STATES: Dict[str, Dict[str, float]] = {
    "automotive_lacquer": {
        "specularity": 0.95,
        "micro_texture_density": 0.02,
        "material_hardness": 0.85,
        "organic_synthetic_ratio": 0.00,
        "surface_pattern_scale": 0.05,
    },
    "beaded_textile": {
        "specularity": 0.45,
        "micro_texture_density": 0.90,
        "material_hardness": 0.35,
        "organic_synthetic_ratio": 0.20,
        "surface_pattern_scale": 0.40,
    },
    "matte_ceramic": {
        "specularity": 0.10,
        "micro_texture_density": 0.08,
        "material_hardness": 0.90,
        "organic_synthetic_ratio": 0.15,
        "surface_pattern_scale": 0.00,
    },
    "waxy_botanical": {
        "specularity": 0.55,
        "micro_texture_density": 0.15,
        "material_hardness": 0.40,
        "organic_synthetic_ratio": 0.95,
        "surface_pattern_scale": 0.30,
    },
    "spiky_seedcoat": {
        "specularity": 0.15,
        "micro_texture_density": 0.95,
        "material_hardness": 0.75,
        "organic_synthetic_ratio": 1.00,
        "surface_pattern_scale": 0.55,
    },
    "polished_stone": {
        "specularity": 0.80,
        "micro_texture_density": 0.05,
        "material_hardness": 0.95,
        "organic_synthetic_ratio": 0.70,
        "surface_pattern_scale": 0.65,
    },
    "woven_fiber": {
        "specularity": 0.10,
        "micro_texture_density": 0.70,
        "material_hardness": 0.15,
        "organic_synthetic_ratio": 0.80,
        "surface_pattern_scale": 0.75,
    },
    "liquid_chrome": {
        "specularity": 1.00,
        "micro_texture_density": 0.00,
        "material_hardness": 0.70,
        "organic_synthetic_ratio": 0.00,
        "surface_pattern_scale": 0.00,
    },
    "frosted_glass": {
        "specularity": 0.25,
        "micro_texture_density": 0.50,
        "material_hardness": 0.85,
        "organic_synthetic_ratio": 0.05,
        "surface_pattern_scale": 0.10,
    },
}

# ============================================================================
# Constants: Rhythmic Presets
# ============================================================================

RHYTHMIC_PRESETS = {
    "sheen_oscillation": {
        "period": 15,
        "state_a": "matte_ceramic",
        "state_b": "automotive_lacquer",
        "pattern": "sinusoidal",
        "description": "Matte to mirror finish sweep — dead flat absorption to deep automotive gloss",
    },
    "texture_accretion": {
        "period": 19,
        "state_a": "liquid_chrome",
        "state_b": "spiky_seedcoat",
        "pattern": "triangular",
        "description": (
            "Smooth to maximum texture density — chrome mirror to spiny organic armor. "
            "Prime period creates complex irrational beats with all neighbors"
        ),
    },
    "material_softening": {
        "period": 21,
        "state_a": "polished_stone",
        "state_b": "woven_fiber",
        "pattern": "sinusoidal",
        "description": "Rigid mineral to soft textile — hard polished surface yielding to draped woven cloth",
    },
    "nature_synthesis": {
        "period": 24,
        "state_a": "automotive_lacquer",
        "state_b": "waxy_botanical",
        "pattern": "sinusoidal",
        "description": (
            "Industrial synthetic to living organic — factory clearcoat dissolving into leaf cuticle. "
            "Syncs with microscopy focus_sweep for micro-to-macro surface inspection"
        ),
    },
    "full_palette_morph": {
        "period": 30,
        "state_a": "frosted_glass",
        "state_b": "beaded_textile",
        "pattern": "sinusoidal",
        "description": (
            "Translucent mineral to opaque embellished textile — maximum surface diversity. "
            "MAJOR LCM HUB for full-system synchronization"
        ),
    },
}

# ============================================================================
# Constants: Visual Vocabulary
# ============================================================================

VISUAL_VOCABULARY = {
    "finish": [
        "deep automotive clearcoat with mirror-depth reflections",
        "wet-look lacquer gloss catching environmental light",
        "satin semi-gloss with soft directional highlights",
        "eggshell finish absorbing light with faint sheen",
        "chalk matte fully absorbent zero-reflection surface",
        "raw unfinished material showing natural porosity",
        "pearlescent color-shifting iridescent coating",
        "anodized metal with colored oxide layer",
    ],
    "micro_texture": [
        "glass-smooth polished to optical flatness",
        "fine stipple texture like orange peel at close range",
        "raised dot matrix beaded surface catching light at each point",
        "densely studded micro-protrusions creating shadow fields",
        "tightly packed bristle array with uniform fiber direction",
        "pebbled grain leather-like dimpled surface",
        "hammered metal with irregular concavity pattern",
        "sandblasted matte micro-roughness scattering all light",
    ],
    "material_character": [
        "rigid porcelain with brittle fracture edges",
        "injection-molded polymer with uniform density",
        "hand-thrown stoneware with slight surface undulation",
        "supple draped fabric following gravity",
        "stiff architectural felt holding sculptural form",
        "flexible silicone with elastic surface memory",
        "crystalline mineral with planar cleavage faces",
        "fibrous wood grain with directional strength",
    ],
    "organic_surface": [
        "waxy leaf cuticle with hydrophobic beading",
        "bark texture with deep fissure channels",
        "seed pod armor with conical spike protrusions",
        "petal surface with microscopic velvet papillae",
        "insect chitin with layered structural color",
        "eggshell calcium carbonate micro-pore texture",
        "mushroom cap surface with hygroscopic moisture sheen",
        "coral skeleton with porous calcium lattice",
    ],
    "synthetic_surface": [
        "automotive body panel with multi-layer paint system",
        "chrome-plated steel with mirror-perfect electrodeposition",
        "carbon fiber weave visible under clear resin",
        "brushed aluminum with unidirectional grain lines",
        "powder-coated matte industrial finish",
        "blown glass with internal bubble inclusions",
        "cast concrete with aggregate texture and formwork marks",
        "3D-printed layer lines with visible deposition ridges",
    ],
    "pattern_scale": [
        "uniform monochrome with no visible pattern",
        "micro-pattern visible only at close inspection",
        "small-scale repeat tile like mosaic or chainmail",
        "medium-scale motif with clear figure-ground rhythm",
        "large-scale graphic pattern dominating the surface",
        "irregular organic distribution like lichen or rust",
        "gradient transition with no discrete repeat boundary",
        "fractal self-similar pattern at multiple zoom levels",
    ],
    "light_interaction": [
        "total specular reflection doubling the environment",
        "broad diffuse highlight spreading across curved form",
        "subsurface scattering with internal glow through thin material",
        "retroreflective surface bouncing light back to source",
        "light-trapping surface absorbing nearly all incident photons",
        "structural color from thin-film interference shifting with angle",
        "translucent edge-lit glow at material boundaries",
        "caustic light pattern projected through transparent material",
    ],
    "color_palette": [
        "raw material natural color — bone white, clay red, wood brown",
        "industrial neutral — gunmetal gray, matte black, white primer",
        "automotive candy — deep candy apple red, electric blue, pearl white",
        "botanical palette — chlorophyll green, petal pink, pollen gold",
        "mineral spectrum — obsidian black, marble white, slate blue-gray",
        "oxidation tones — verdigris green, rust orange, tarnished brass",
    ],
}

# ============================================================================
# Visual Type Mapping (nearest-neighbor for vocabulary extraction)
# ============================================================================

VISUAL_TYPES = {
    "mirror_gloss": {
        "center": {"specularity": 0.95, "micro_texture_density": 0.05, "material_hardness": 0.80,
                    "organic_synthetic_ratio": 0.05, "surface_pattern_scale": 0.05},
        "keywords": ["mirror-depth reflections", "wet-look lacquer gloss", "chrome-plated electrodeposition",
                      "total specular reflection", "automotive clearcoat"],
        "optical": {"finish": "specular", "scatter": "none", "transparency": "opaque"},
        "color_associations": ["chrome silver", "candy apple red", "piano black", "pearl white"],
    },
    "matte_mineral": {
        "center": {"specularity": 0.10, "micro_texture_density": 0.10, "material_hardness": 0.90,
                    "organic_synthetic_ratio": 0.20, "surface_pattern_scale": 0.10},
        "keywords": ["chalk matte fully absorbent surface", "rigid porcelain brittle edges",
                      "sandblasted micro-roughness", "powder-coated matte finish", "cast concrete aggregate"],
        "optical": {"finish": "matte", "scatter": "full_diffuse", "transparency": "opaque"},
        "color_associations": ["chalk white", "concrete gray", "terracotta", "gunmetal"],
    },
    "textured_embellished": {
        "center": {"specularity": 0.40, "micro_texture_density": 0.85, "material_hardness": 0.35,
                    "organic_synthetic_ratio": 0.25, "surface_pattern_scale": 0.50},
        "keywords": ["raised dot matrix beaded surface", "densely studded micro-protrusions",
                      "small-scale repeat tile mosaic chainmail", "pebbled grain dimpled surface",
                      "hammered metal irregular concavity"],
        "optical": {"finish": "semi-gloss", "scatter": "micro_faceted", "transparency": "opaque"},
        "color_associations": ["metallic gold bead", "iridescent sequin", "hammered copper", "mosaic tile"],
    },
    "organic_botanical": {
        "center": {"specularity": 0.40, "micro_texture_density": 0.30, "material_hardness": 0.45,
                    "organic_synthetic_ratio": 0.95, "surface_pattern_scale": 0.35},
        "keywords": ["waxy leaf cuticle hydrophobic beading", "petal velvet papillae",
                      "mushroom cap hygroscopic sheen", "bark deep fissure channels",
                      "botanical palette chlorophyll green pollen gold"],
        "optical": {"finish": "waxy_sheen", "scatter": "subsurface", "transparency": "translucent_edges"},
        "color_associations": ["chlorophyll green", "petal pink", "pollen gold", "bark brown"],
    },
    "spiny_armor": {
        "center": {"specularity": 0.15, "micro_texture_density": 0.95, "material_hardness": 0.80,
                    "organic_synthetic_ratio": 0.90, "surface_pattern_scale": 0.55},
        "keywords": ["seed pod armor conical spike protrusions", "insect chitin layered structural color",
                      "coral skeleton porous calcium lattice", "tightly packed bristle array",
                      "eggshell calcium carbonate micro-pore"],
        "optical": {"finish": "matte_rough", "scatter": "shadow_field", "transparency": "opaque"},
        "color_associations": ["chitin bronze", "seed pod brown", "coral white", "spine dark"],
    },
    "soft_woven": {
        "center": {"specularity": 0.10, "micro_texture_density": 0.65, "material_hardness": 0.15,
                    "organic_synthetic_ratio": 0.75, "surface_pattern_scale": 0.70},
        "keywords": ["supple draped fabric following gravity", "stiff architectural felt",
                      "fibrous wood grain directional strength", "carbon fiber weave under clear resin",
                      "fractal self-similar pattern multiple zoom levels"],
        "optical": {"finish": "matte_soft", "scatter": "fiber_diffuse", "transparency": "opaque"},
        "color_associations": ["linen natural", "wool cream", "hemp gray", "woven earth"],
    },
    "translucent_diffuse": {
        "center": {"specularity": 0.30, "micro_texture_density": 0.40, "material_hardness": 0.80,
                    "organic_synthetic_ratio": 0.10, "surface_pattern_scale": 0.10},
        "keywords": ["frosted glass translucent diffusion", "subsurface scattering internal glow",
                      "blown glass internal bubble inclusions", "translucent edge-lit glow",
                      "eggshell finish absorbing light faint sheen"],
        "optical": {"finish": "frosted", "scatter": "volume", "transparency": "translucent"},
        "color_associations": ["frosted white", "sea glass", "milky opal", "ice blue"],
    },
}

# ============================================================================
# Constants: Attractor Presets (Tier 4D Discoveries)
# ============================================================================
#
# Discovered multi-domain emergent attractors from compositional limit cycle
# analysis. Each preset encodes the surface design parameter state that arises
# when the system locks into that attractor period during multi-domain
# composition.
#
# Surface design coordinates are derived from the preset trajectory states
# that dominate each attractor basin — the time-averaged parameter position
# along the limit cycle orbit.
#
# Classification:
#   lcm_sync  — Least Common Multiple synchronization across 3+ domains
#   novel     — Emergent period not explainable by LCM or harmonics
#   harmonic  — Integer multiple of individual domain periods
#   curated   — Hand-selected edge states for specific aesthetic effects

ATTRACTOR_PRESETS = {
    # ── Tier 1: Stable Cores (deploy immediately) ─────────────────────
    "period_30": {
        "name": "Period 30 — Universal Sync",
        "description": (
            "Dominant LCM synchronization across microscopy, diatom, heraldic, "
            "and surface design. The full_palette_morph preset (period 30) locks "
            "directly into this attractor. Most stable across domain additions."
        ),
        "basin_size": 0.116,
        "classification": "lcm_sync",
        "source_domains": ["microscopy", "diatom", "heraldic", "surface_design"],
        "state": {
            "specularity": 0.35,
            "micro_texture_density": 0.46,
            "material_hardness": 0.60,
            "organic_synthetic_ratio": 0.13,
            "surface_pattern_scale": 0.25,
        },
    },
    "period_29": {
        "name": "Period 29 — Emergent Resonance",
        "description": (
            "Purely emergent attractor discovered only in 5-domain composition. "
            "Surface sits between frosted glass and botanical — translucent "
            "organic quality that exists nowhere in individual domain aesthetics."
        ),
        "basin_size": 0.084,
        "classification": "lcm_sync",
        "source_domains": ["microscopy", "nuclear", "catastrophe", "diatom", "heraldic"],
        "state": {
            "specularity": 0.42,
            "micro_texture_density": 0.28,
            "material_hardness": 0.52,
            "organic_synthetic_ratio": 0.48,
            "surface_pattern_scale": 0.18,
        },
    },
    "period_19": {
        "name": "Period 19 — Gap Flow",
        "description": (
            "Resilient novel gap-filler between periods 18 and 20. Surface "
            "texture_accretion preset (period 19) resonates directly. "
            "Stable across 4- and 5-domain systems — fundamental aesthetic "
            "intermediate state with prime-period irrational beat character."
        ),
        "basin_size": 0.074,
        "classification": "novel",
        "source_domains": ["microscopy", "nuclear", "catastrophe", "diatom"],
        "state": {
            "specularity": 0.58,
            "micro_texture_density": 0.48,
            "material_hardness": 0.73,
            "organic_synthetic_ratio": 0.50,
            "surface_pattern_scale": 0.28,
        },
    },
    # ── Tier 2: Specialized (A/B test) ────────────────────────────────
    "period_28": {
        "name": "Period 28 — Composite Beat",
        "description": (
            "Novel composite beat mechanism: Period 60 − 2×Period 16 = 28. "
            "First evidence of attractor-attractor interaction. Surface shows "
            "tension between polished synthetic and organic texture — "
            "the material equivalent of held breath before a phase change."
        ),
        "basin_size": 0.024,
        "classification": "novel",
        "source_domains": ["microscopy", "nuclear", "catastrophe", "diatom"],
        "state": {
            "specularity": 0.62,
            "micro_texture_density": 0.35,
            "material_hardness": 0.68,
            "organic_synthetic_ratio": 0.30,
            "surface_pattern_scale": 0.22,
        },
    },
    "period_60": {
        "name": "Period 60 — Harmonic Hub",
        "description": (
            "Major LCM hub in 4-domain systems (3×20, 4×15, 5×12). "
            "Weakened in 5-domain but still present. Surface oscillates "
            "through full material palette — every canonical state gets "
            "a moment in the cycle. Complex synchronization for advanced use."
        ),
        "basin_size": 0.040,
        "classification": "harmonic",
        "source_domains": ["microscopy", "nuclear", "catastrophe", "diatom"],
        "state": {
            "specularity": 0.50,
            "micro_texture_density": 0.40,
            "material_hardness": 0.55,
            "organic_synthetic_ratio": 0.38,
            "surface_pattern_scale": 0.30,
        },
    },
    # ── Tier 3: Curated Edge States ───────────────────────────────────
    "bifurcation_edge": {
        "name": "Bifurcation Edge — Cusp Threshold",
        "description": (
            "Curated state at the boundary between mirror_gloss and "
            "matte_mineral basins. Surface is poised between specular "
            "and absorbent — the exact moment lacquer begins to frost."
        ),
        "basin_size": None,
        "classification": "curated",
        "source_domains": ["surface_design"],
        "state": {
            "specularity": 0.52,
            "micro_texture_density": 0.06,
            "material_hardness": 0.87,
            "organic_synthetic_ratio": 0.10,
            "surface_pattern_scale": 0.07,
        },
    },
    "organic_complexity": {
        "name": "Organic Complexity — Emergence Bloom",
        "description": (
            "Curated state at maximum organic complexity. Surface is "
            "a living botanical armor — waxy sheen over dense micro-spines, "
            "like a seed pod moments before it opens."
        ),
        "basin_size": None,
        "classification": "curated",
        "source_domains": ["surface_design"],
        "state": {
            "specularity": 0.35,
            "micro_texture_density": 0.72,
            "material_hardness": 0.55,
            "organic_synthetic_ratio": 0.92,
            "surface_pattern_scale": 0.48,
        },
    },
}


# ============================================================================
# Decomposition Engine — text description → 5D coordinates (Layer 2, 0 tokens)
# ============================================================================

_STOP_WORDS = frozenset({
    'a','an','the','in','on','at','to','of','for','with','by','from','and',
    'or','but','as','is','are','was','were','be','been','being','has','have',
    'had','do','does','did','no','not','all','its','this','that','into','over',
})

def _decompose_tokenize(text: str):
    lower = text.lower()
    words = set(re.findall(r'[a-z]+(?:-[a-z]+)*', lower))
    return words, lower

def _decompose_extract_fragments(keyword: str) -> list:
    words = keyword.lower().split()
    frags = []
    if len(words) >= 3:
        frags.append(keyword.lower())
    for ws in [4, 3, 2]:
        for i in range(len(words) - ws + 1):
            frag = ' '.join(words[i:i + ws])
            content = [w for w in words[i:i + ws] if len(w) > 3 and w not in _STOP_WORDS]
            if content:
                frags.append(frag)
    return frags

def _decompose_score_type(vtype_data: dict, words: set, full_text: str):
    score = 0.0
    matched = []
    for kw in vtype_data.get("keywords", []):
        frags = _decompose_extract_fragments(kw)
        best_s, best_f = 0.0, None
        for f in frags:
            if f in full_text:
                if 1.0 > best_s:
                    best_s, best_f = 1.0, f
            else:
                fw = set(f.split()) - _STOP_WORDS
                if fw:
                    olap = len(fw & words) / len(fw)
                    ws = olap * 0.3
                    if ws > best_s:
                        best_s, best_f = ws, f
        if best_f and best_s > 0:
            score += best_s
            matched.append(best_f)
    for pn, pv in vtype_data.get("optical", {}).items():
        pw = set(pv.lower().replace('_', ' ').split())
        po = len(pw & words)
        if po > 0:
            score += 0.5 * (po / len(pw))
            matched.append(f"optical:{pv}")
    for c in vtype_data.get("color_associations", []):
        cl = c.lower()
        if cl in full_text:
            score += 0.4
            matched.append(f"color:{c}")
        else:
            cw = set(cl.split()) - _STOP_WORDS
            if cw and len(cw & words) > 0:
                score += 0.2 * (len(cw & words) / len(cw))
    return score, matched

def _decompose_softmax(scores: dict) -> dict:
    if not scores or max(scores.values()) == 0:
        n = len(scores)
        return {k: 1.0 / n for k in scores} if n else {}
    t = 1.5
    mx = max(scores.values())
    exps = {k: math.exp((v - mx) / t) for k, v in scores.items()}
    total = sum(exps.values())
    return {k: v / total for k, v in exps.items()}

def _decompose_blend(weights: dict) -> dict:
    result = {p: 0.0 for p in PARAMETER_NAMES}
    for vid, vdata in VISUAL_TYPES.items():
        w = weights.get(vid, 0)
        if w > 0:
            for p in PARAMETER_NAMES:
                result[p] += w * vdata["center"].get(p, 0)
    return result

def _decompose_description(description: str) -> dict:
    """Core decomposition: text → 5D coordinates via keyword matching."""
    words, full_text = _decompose_tokenize(description)
    type_scores = {}
    all_matched = []
    optical_matches = {}
    for vid, vdata in VISUAL_TYPES.items():
        sc, mt = _decompose_score_type(vdata, words, full_text)
        type_scores[vid] = sc
        all_matched.extend(mt)
        for m in mt:
            if m.startswith("optical:"):
                val = m.split(":", 1)[1]
                for pn, pv in vdata.get("optical", {}).items():
                    if pv == val:
                        optical_matches[pn] = val
    color_matches = [m.split(":", 1)[1] for m in all_matched if m.startswith("color:")]
    max_score = max(type_scores.values()) if type_scores else 0
    nkw = len(next(iter(VISUAL_TYPES.values()))["keywords"]) if VISUAL_TYPES else 5
    max_possible = nkw * 1.0 + 3 * 0.5 + 4 * 0.4
    confidence = min(1.0, max_score / max_possible) if max_possible > 0 else 0.0
    if confidence < 0.05:
        return {
            "coordinates": {p: 0.5 for p in PARAMETER_NAMES},
            "confidence": 0.0, "nearest_type": "",
            "type_scores": type_scores, "type_weights": {},
            "matched_fragments": [], "optical_match": {}, "color_matches": [],
        }
    weights = _decompose_softmax(type_scores)
    coords = _decompose_blend(weights)
    nearest = max(type_scores, key=type_scores.get)
    nc = VISUAL_TYPES[nearest]["center"]
    dist = math.sqrt(sum((coords.get(p, 0) - nc.get(p, 0)) ** 2 for p in PARAMETER_NAMES))
    unique_frags = list(dict.fromkeys(
        m for m in all_matched if not m.startswith(("optical:", "color:"))
    ))
    return {
        "coordinates": {k: round(v, 4) for k, v in coords.items()},
        "confidence": round(confidence, 4),
        "nearest_type": nearest,
        "nearest_type_distance": round(dist, 4),
        "type_scores": {k: round(v, 3) for k, v in type_scores.items()},
        "type_weights": {k: round(v, 4) for k, v in weights.items()},
        "matched_fragments": unique_frags,
        "optical_match": optical_matches,
        "color_matches": color_matches,
    }

def _decompose_round_trip_fidelity() -> dict:
    """Test fidelity by round-tripping each visual type through its own keywords."""
    results = []
    for vid, vdata in VISUAL_TYPES.items():
        desc = ". ".join(vdata["keywords"])
        r = _decompose_description(desc)
        errs = {p: abs(vdata["center"].get(p, 0) - r["coordinates"].get(p, 0))
                for p in PARAMETER_NAMES}
        avg_err = sum(errs.values()) / len(errs)
        results.append({
            "type_id": vid, "confidence": r["confidence"],
            "nearest_type": r["nearest_type"],
            "correct": r["nearest_type"] == vid,
            "reconstruction_error": round(avg_err, 4),
            "matched_count": len(r["matched_fragments"]),
        })
    correct = sum(1 for r in results if r["correct"])
    avg_e = sum(r["reconstruction_error"] for r in results) / len(results) if results else 0
    return {
        "total_types": len(results), "correct_count": correct,
        "accuracy": round(correct / len(results), 3) if results else 0,
        "mean_error": round(avg_e, 4), "per_type": results,
    }


# ============================================================================
# Helper Functions
# ============================================================================

def _euclidean_distance(a: Dict[str, float], b: Dict[str, float]) -> float:
    """Euclidean distance between two states in parameter space."""
    return math.sqrt(sum((a[p] - b[p]) ** 2 for p in PARAMETER_NAMES))


def _nearest_canonical(state: Dict[str, float]) -> tuple:
    """Find nearest canonical state. Returns (state_id, distance)."""
    best_id, best_dist = None, float("inf")
    for sid, coords in CANONICAL_STATES.items():
        d = _euclidean_distance(state, coords)
        if d < best_dist:
            best_id, best_dist = sid, d
    return best_id, best_dist


def _nearest_visual_type(state: Dict[str, float]) -> tuple:
    """Find nearest visual type. Returns (type_id, distance)."""
    best_id, best_dist = None, float("inf")
    for vid, vdata in VISUAL_TYPES.items():
        d = _euclidean_distance(state, vdata["center"])
        if d < best_dist:
            best_id, best_dist = vid, d
    return best_id, best_dist


def _interpolate_states(
    state_a: Dict[str, float],
    state_b: Dict[str, float],
    t: float,
    pattern: str = "sinusoidal",
) -> Dict[str, float]:
    """Interpolate between two states at phase t ∈ [0, 1]."""
    if pattern == "sinusoidal":
        alpha = 0.5 * (1.0 - math.cos(math.pi * t))
    elif pattern == "triangular":
        alpha = 2.0 * t if t <= 0.5 else 2.0 * (1.0 - t)
    elif pattern == "square":
        alpha = 0.0 if t < 0.5 else 1.0
    else:
        alpha = t  # linear fallback

    return {
        p: state_a[p] + alpha * (state_b[p] - state_a[p]) for p in PARAMETER_NAMES
    }


def _select_vocabulary(state: Dict[str, float]) -> Dict[str, List[str]]:
    """Select vocabulary terms weighted by parameter values."""
    selected = {}
    n_terms = len(list(VISUAL_VOCABULARY.values())[0])

    for category, terms in VISUAL_VOCABULARY.items():
        # Map primary parameter to index
        if category == "finish":
            idx = round(state["specularity"] * (len(terms) - 1))
        elif category == "micro_texture":
            idx = round(state["micro_texture_density"] * (len(terms) - 1))
        elif category == "material_character":
            idx = round(state["material_hardness"] * (len(terms) - 1))
        elif category == "organic_surface":
            idx = round(state["organic_synthetic_ratio"] * (len(terms) - 1))
        elif category == "synthetic_surface":
            idx = round((1.0 - state["organic_synthetic_ratio"]) * (len(terms) - 1))
        elif category == "pattern_scale":
            idx = round(state["surface_pattern_scale"] * (len(terms) - 1))
        elif category == "light_interaction":
            idx = round(state["specularity"] * (len(terms) - 1))
        elif category == "color_palette":
            idx = round(state["organic_synthetic_ratio"] * (len(terms) - 1))
        else:
            idx = 0

        idx = max(0, min(idx, len(terms) - 1))
        # Return primary + neighbors for blending
        neighbors = [
            terms[max(0, idx - 1)],
            terms[idx],
            terms[min(len(terms) - 1, idx + 1)],
        ]
        selected[category] = list(dict.fromkeys(neighbors))  # deduplicate preserving order

    return selected


# ============================================================================
# Layer 1: Pure Taxonomy Lookups (0 tokens)
# ============================================================================

@mcp.tool(
    name="get_surface_types",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def get_surface_types() -> str:
    """List all 9 canonical surface treatment types with descriptions.

    Layer 1: Pure taxonomy lookup (0 tokens)

    Returns:
        JSON mapping surface type IDs to their 5D parameter coordinates
        and human-readable descriptions.
    """
    result = {}
    descriptions = {
        "automotive_lacquer": "Deep multi-layer clearcoat — maximum specularity, zero texture, fully synthetic",
        "beaded_textile": "Embellished fabric with dense micro-bead surface — moderate gloss, high texture",
        "matte_ceramic": "Unglazed fired clay — zero specularity, zero texture, rigid and mineral",
        "waxy_botanical": "Living plant cuticle — moderate waxy sheen, organic, hydrophobic surface",
        "spiky_seedcoat": "Protective seed armor — dense spike protrusions, fully organic, high texture",
        "polished_stone": "Ground and buffed mineral — high specularity, hard, naturally patterned",
        "woven_fiber": "Interlaced textile — matte, high texture from fiber crossings, soft and pliable",
        "liquid_chrome": "Perfect mirror metal — maximum specularity, zero texture, zero pattern",
        "frosted_glass": "Acid-etched or sandblasted glass — low specularity, medium texture, translucent",
    }

    for state_id, coords in CANONICAL_STATES.items():
        result[state_id] = {
            "description": descriptions.get(state_id, ""),
            "coordinates": coords,
        }

    return json.dumps(result, indent=2)


@mcp.tool(
    name="get_surface_specifications",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def get_surface_specifications(surface_id: str) -> str:
    """Get complete visual specifications for a surface treatment type.

    Layer 1: Pure taxonomy lookup (0 tokens)

    Args:
        surface_id: One of the 9 canonical surface types
            (automotive_lacquer, beaded_textile, matte_ceramic,
             waxy_botanical, spiky_seedcoat, polished_stone,
             woven_fiber, liquid_chrome, frosted_glass)

    Returns:
        Complete visual vocabulary, optical properties, and parameter coordinates.
    """
    if surface_id not in CANONICAL_STATES:
        return json.dumps({
            "error": f"Unknown surface type: {surface_id}",
            "available": list(CANONICAL_STATES.keys()),
        })

    coords = CANONICAL_STATES[surface_id]
    vocab = _select_vocabulary(coords)
    vtype_id, vtype_dist = _nearest_visual_type(coords)
    vtype = VISUAL_TYPES[vtype_id]

    return json.dumps({
        "surface_id": surface_id,
        "coordinates": coords,
        "nearest_visual_type": vtype_id,
        "visual_type_distance": round(vtype_dist, 4),
        "optical_properties": vtype["optical"],
        "vocabulary": vocab,
        "keywords": vtype["keywords"],
    }, indent=2)


# ============================================================================
# Layer 2: Deterministic Computation (0 tokens)
# ============================================================================

@mcp.tool(
    name="map_surface_parameters",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def map_surface_parameters(
    surface_id: str,
    intensity: str = "moderate",
    emphasis: str = "finish",
) -> str:
    """Map surface type to visual parameters for image generation.

    Layer 2: Deterministic operation (0 tokens)

    Args:
        surface_id: Which surface (automotive_lacquer, beaded_textile, etc.)
        intensity: "subtle", "moderate", or "dramatic"
        emphasis: "finish", "texture", "material", "pattern", or "light"

    Returns:
        Complete parameter set for visual synthesis including vocabulary
        weighted by intensity and emphasis.
    """
    if surface_id not in CANONICAL_STATES:
        return json.dumps({
            "error": f"Unknown surface type: {surface_id}",
            "available": list(CANONICAL_STATES.keys()),
        })

    intensity_scale = {"subtle": 0.5, "moderate": 1.0, "dramatic": 1.5}.get(intensity, 1.0)
    coords = CANONICAL_STATES[surface_id]

    # Scale coordinates by intensity (clamped to [0,1])
    scaled = {p: max(0.0, min(1.0, v * intensity_scale)) for p, v in coords.items()}

    # Emphasis boosts specific parameters
    emphasis_map = {
        "finish": "specularity",
        "texture": "micro_texture_density",
        "material": "material_hardness",
        "pattern": "surface_pattern_scale",
        "light": "specularity",
    }
    if emphasis in emphasis_map:
        param = emphasis_map[emphasis]
        scaled[param] = max(0.0, min(1.0, scaled[param] * 1.3))

    vocab = _select_vocabulary(scaled)
    vtype_id, _ = _nearest_visual_type(scaled)
    vtype = VISUAL_TYPES[vtype_id]

    return json.dumps({
        "surface_id": surface_id,
        "intensity": intensity,
        "emphasis": emphasis,
        "parameters": {p: round(v, 4) for p, v in scaled.items()},
        "visual_type": vtype_id,
        "optical_properties": vtype["optical"],
        "vocabulary": vocab,
        "keywords": vtype["keywords"],
    }, indent=2)


@mcp.tool(
    name="compute_surface_distance",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def compute_surface_distance(
    surface_id_1: str,
    surface_id_2: str,
) -> str:
    """Compute distance between two surface treatment types.

    Layer 2: Pure distance computation (0 tokens)

    Args:
        surface_id_1: First surface type
        surface_id_2: Second surface type

    Returns:
        Euclidean distance and per-parameter breakdown.
    """
    if surface_id_1 not in CANONICAL_STATES:
        return json.dumps({"error": f"Unknown: {surface_id_1}", "available": list(CANONICAL_STATES.keys())})
    if surface_id_2 not in CANONICAL_STATES:
        return json.dumps({"error": f"Unknown: {surface_id_2}", "available": list(CANONICAL_STATES.keys())})

    a = CANONICAL_STATES[surface_id_1]
    b = CANONICAL_STATES[surface_id_2]
    dist = _euclidean_distance(a, b)
    deltas = {p: round(b[p] - a[p], 4) for p in PARAMETER_NAMES}

    return json.dumps({
        "surface_1": surface_id_1,
        "surface_2": surface_id_2,
        "euclidean_distance": round(dist, 4),
        "parameter_deltas": deltas,
        "dominant_axis": max(deltas, key=lambda p: abs(deltas[p])),
    }, indent=2)


@mcp.tool(
    name="compute_surface_trajectory",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def compute_surface_trajectory(
    start_surface_id: str,
    end_surface_id: str,
    num_steps: int = 20,
) -> str:
    """Compute smooth trajectory between two surface types in morphospace.

    Layer 2: Deterministic trajectory integration (0 tokens)

    Enables visualization of smooth material transitions — e.g.
    automotive lacquer gradually becoming waxy botanical.

    Args:
        start_surface_id: Starting surface type
        end_surface_id: Target surface type
        num_steps: Number of interpolation steps (default: 20)

    Returns:
        Trajectory with intermediate states, distance profile,
        and transition characteristics.
    """
    if start_surface_id not in CANONICAL_STATES:
        return json.dumps({"error": f"Unknown: {start_surface_id}"})
    if end_surface_id not in CANONICAL_STATES:
        return json.dumps({"error": f"Unknown: {end_surface_id}"})

    a = CANONICAL_STATES[start_surface_id]
    b = CANONICAL_STATES[end_surface_id]
    total_dist = _euclidean_distance(a, b)

    trajectory = []
    for i in range(num_steps + 1):
        t = i / num_steps
        state = {p: round(a[p] + t * (b[p] - a[p]), 4) for p in PARAMETER_NAMES}
        nearest_id, nearest_dist = _nearest_canonical(state)
        trajectory.append({
            "step": i,
            "t": round(t, 4),
            "state": state,
            "nearest_canonical": nearest_id,
            "distance_from_nearest": round(nearest_dist, 4),
        })

    # Characterize the transition
    deltas = {p: round(b[p] - a[p], 4) for p in PARAMETER_NAMES}
    increasing = [p for p, d in deltas.items() if d > 0.1]
    decreasing = [p for p, d in deltas.items() if d < -0.1]

    return json.dumps({
        "start_surface": start_surface_id,
        "end_surface": end_surface_id,
        "total_distance": round(total_dist, 4),
        "num_steps": num_steps,
        "trajectory": trajectory,
        "transition_characteristics": {
            "increasing_parameters": increasing,
            "decreasing_parameters": decreasing,
            "dominant_axis": max(deltas, key=lambda p: abs(deltas[p])),
            "parameter_deltas": deltas,
        },
    }, indent=2)


# ============================================================================
# Layer 2: Rhythmic Composition (Phase 2.6)
# ============================================================================

@mcp.tool(
    name="list_surface_rhythmic_presets",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def list_surface_rhythmic_presets() -> str:
    """List all available surface design rhythmic presets.

    Layer 2: Pure lookup (0 tokens)

    Returns:
        Preset names, periods, patterns, and descriptions.
    """
    return json.dumps(RHYTHMIC_PRESETS, indent=2)


@mcp.tool(
    name="apply_surface_rhythmic_preset",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def apply_surface_rhythmic_preset(preset_name: str) -> str:
    """Apply curated surface design rhythmic pattern preset.

    Layer 2: Deterministic sequence generation (0 tokens)

    Available presets:
        sheen_oscillation (15): matte ↔ mirror
        texture_accretion (19): smooth ↔ spiky (prime period)
        material_softening (21): stone ↔ woven
        nature_synthesis (24): synthetic ↔ organic
        full_palette_morph (30): glass ↔ textile (LCM hub)

    Args:
        preset_name: One of the 5 rhythmic presets

    Returns:
        Complete oscillation sequence with parameter states at each step.
    """
    if preset_name not in RHYTHMIC_PRESETS:
        return json.dumps({
            "error": f"Unknown preset: {preset_name}",
            "available": list(RHYTHMIC_PRESETS.keys()),
        })

    preset = RHYTHMIC_PRESETS[preset_name]
    state_a = CANONICAL_STATES[preset["state_a"]]
    state_b = CANONICAL_STATES[preset["state_b"]]
    period = preset["period"]
    pattern = preset["pattern"]

    # Generate one full cycle
    sequence = []
    for step in range(period):
        t = step / period
        state = _interpolate_states(state_a, state_b, t * 2 if t <= 0.5 else 2 * (1 - t), pattern)
        nearest_id, _ = _nearest_canonical(state)
        sequence.append({
            "step": step,
            "phase": round(t, 4),
            "state": {p: round(v, 4) for p, v in state.items()},
            "nearest_canonical": nearest_id,
        })

    return json.dumps({
        "preset": preset_name,
        "period": period,
        "pattern": pattern,
        "state_a": preset["state_a"],
        "state_b": preset["state_b"],
        "description": preset["description"],
        "sequence": sequence,
    }, indent=2)


@mcp.tool(
    name="generate_surface_rhythmic_sequence",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def generate_surface_rhythmic_sequence(
    state_a_id: str,
    state_b_id: str,
    oscillation_pattern: str = "sinusoidal",
    num_cycles: int = 3,
    steps_per_cycle: int = 20,
    phase_offset: float = 0.0,
) -> str:
    """Generate rhythmic oscillation between two surface types.

    Layer 2: Temporal composition (0 tokens)

    Args:
        state_a_id: Starting surface type
        state_b_id: Alternating surface type
        oscillation_pattern: "sinusoidal", "triangular", or "square"
        num_cycles: Number of complete A→B→A cycles
        steps_per_cycle: Samples per cycle
        phase_offset: Starting phase (0.0 = A, 0.5 = B)

    Returns:
        Sequence with states, pattern info, and phase points.
    """
    if state_a_id not in CANONICAL_STATES:
        return json.dumps({"error": f"Unknown: {state_a_id}"})
    if state_b_id not in CANONICAL_STATES:
        return json.dumps({"error": f"Unknown: {state_b_id}"})

    state_a = CANONICAL_STATES[state_a_id]
    state_b = CANONICAL_STATES[state_b_id]
    total_steps = num_cycles * steps_per_cycle

    sequence = []
    for step in range(total_steps):
        raw_phase = (step / steps_per_cycle + phase_offset) % 1.0
        # Convert to A→B→A within one cycle
        t = raw_phase * 2 if raw_phase <= 0.5 else 2 * (1 - raw_phase)
        state = _interpolate_states(state_a, state_b, t, oscillation_pattern)
        sequence.append({
            "step": step,
            "cycle": step // steps_per_cycle,
            "phase": round(raw_phase, 4),
            "state": {p: round(v, 4) for p, v in state.items()},
        })

    return json.dumps({
        "state_a": state_a_id,
        "state_b": state_b_id,
        "pattern": oscillation_pattern,
        "num_cycles": num_cycles,
        "steps_per_cycle": steps_per_cycle,
        "total_steps": total_steps,
        "sequence": sequence,
    }, indent=2)


# ============================================================================
# Layer 2: Visual Vocabulary Extraction (Phase 2.7)
# ============================================================================

@mcp.tool(
    name="extract_surface_visual_vocabulary",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def extract_surface_visual_vocabulary(
    state: Optional[Dict[str, float]] = None,
    surface_id: Optional[str] = None,
    strength: float = 1.0,
) -> str:
    """Extract visual vocabulary from surface parameter coordinates.

    Layer 2: Deterministic vocabulary mapping (0 tokens)

    Maps a 5D parameter state to the nearest visual type and returns
    image-generation-ready keywords.

    Args:
        state: Parameter coordinates dict (specularity, micro_texture_density, etc.)
            Provide either state or surface_id.
        surface_id: Canonical surface type to use as state source.
        strength: Keyword weight multiplier [0.0, 1.0] (default: 1.0)

    Returns:
        Nearest visual type, keywords, optical properties, and vocabulary.
    """
    if state is None and surface_id is None:
        return json.dumps({"error": "Provide either 'state' or 'surface_id'"})

    if surface_id is not None:
        if surface_id not in CANONICAL_STATES:
            return json.dumps({"error": f"Unknown: {surface_id}"})
        state = CANONICAL_STATES[surface_id]

    # Validate state keys
    missing = [p for p in PARAMETER_NAMES if p not in state]
    if missing:
        return json.dumps({"error": f"Missing parameters: {missing}", "required": PARAMETER_NAMES})

    vtype_id, vtype_dist = _nearest_visual_type(state)
    vtype = VISUAL_TYPES[vtype_id]
    vocab = _select_vocabulary(state)

    return json.dumps({
        "nearest_type": vtype_id,
        "distance": round(vtype_dist, 4),
        "keywords": vtype["keywords"],
        "optical_properties": vtype["optical"],
        "vocabulary": vocab,
        "strength": strength,
        "state": {p: round(v, 4) for p, v in state.items()},
    }, indent=2)


@mcp.tool(
    name="decompose_surface_from_description",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def decompose_surface_from_description(
    description: str,
    include_fidelity_test: bool = False,
) -> str:
    """Decompose a text description into surface design 5D coordinates.

    Layer 2: Deterministic, 0 LLM tokens.

    Inverse of the generative pipeline — completes the round-trip:
        coordinates → prompt → image → description → coordinates

    Uses keyword fragment matching against the 7 visual types to score
    how much of the surface design vocabulary is present, then blends
    type centers via softmax-weighted average to recover coordinates.

    Args:
        description: Image description text (from Claude vision output,
            user description, or any text describing an aesthetic artifact).
        include_fidelity_test: If True, also runs round-trip fidelity
            validation on all visual types (for diagnostics).

    Returns:
        JSON with coordinates, confidence, nearest_type, type_scores,
        type_weights, matched_fragments, optical_match, color_matches.

    Cost: 0 tokens (pure keyword matching + arithmetic blending)

    Example:
        >>> decompose_surface_from_description(
        ...     "mirror-depth reflections on automotive clearcoat, "
        ...     "chrome-plated surface with total specular reflection"
        ... )
        {
            "coordinates": {"specularity": 0.92, ...},
            "confidence": 0.78,
            "nearest_type": "mirror_gloss",
            ...
        }
    """
    result = _decompose_description(description)

    if include_fidelity_test:
        result["fidelity_test"] = _decompose_round_trip_fidelity()

    return json.dumps(result, indent=2)


@mcp.tool(
    name="generate_surface_prompt",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def generate_surface_prompt(
    surface_id: str = "",
    custom_state: Optional[Dict[str, float]] = None,
    mode: str = "composite",
    style_modifier: str = "",
) -> str:
    """Generate image generation prompt from surface state or canonical type.

    Layer 2: Deterministic prompt synthesis (0 tokens)

    Translates surface design coordinates into visual prompts suitable
    for ComfyUI, Stable Diffusion, DALL-E, etc.

    Args:
        surface_id: Canonical surface type (or "" with custom_state)
        custom_state: Optional custom 5D coordinates
        mode: "composite" (single blended prompt) or "split_view" (per-category)
        style_modifier: Optional prefix ("photorealistic", "oil painting", etc.)

    Returns:
        Prompt string(s) with vocabulary details and surface metadata.
    """
    if custom_state is not None:
        state = custom_state
    elif surface_id and surface_id in CANONICAL_STATES:
        state = CANONICAL_STATES[surface_id]
    else:
        return json.dumps({
            "error": "Provide surface_id or custom_state",
            "available_surfaces": list(CANONICAL_STATES.keys()),
        })

    vtype_id, vtype_dist = _nearest_visual_type(state)
    vtype = VISUAL_TYPES[vtype_id]
    vocab = _select_vocabulary(state)

    if mode == "composite":
        # Build single blended prompt from all vocabulary categories
        parts = []
        if style_modifier:
            parts.append(style_modifier)

        # Primary keywords from visual type
        parts.extend(vtype["keywords"][:3])

        # One term from each vocabulary category
        for cat, terms in vocab.items():
            if terms:
                parts.append(terms[1] if len(terms) > 1 else terms[0])

        # Optical properties
        optical = vtype["optical"]
        parts.append(f"{optical['finish']} finish, {optical['scatter']} light scatter")

        prompt = ", ".join(parts)

        return json.dumps({
            "mode": "composite",
            "prompt": prompt,
            "surface": surface_id or "custom",
            "visual_type": vtype_id,
            "vocabulary": vocab,
        }, indent=2)

    elif mode == "split_view":
        panels = {}
        for cat, terms in vocab.items():
            panel_parts = []
            if style_modifier:
                panel_parts.append(style_modifier)
            panel_parts.extend(terms)
            panels[cat] = ", ".join(panel_parts)

        return json.dumps({
            "mode": "split_view",
            "panels": panels,
            "surface": surface_id or "custom",
            "visual_type": vtype_id,
        }, indent=2)

    else:
        return json.dumps({"error": f"Unknown mode: {mode}. Use 'composite' or 'split_view'"})


@mcp.tool(
    name="generate_surface_sequence_prompts",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def generate_surface_sequence_prompts(
    preset_name: str,
    keyframe_count: int = 4,
    style_modifier: str = "",
) -> str:
    """Generate keyframe prompts from a rhythmic preset.

    Layer 2: Deterministic keyframe extraction (0 tokens)

    Extracts evenly-spaced keyframes from a rhythmic oscillation
    and generates an image prompt for each. Useful for storyboards,
    animation keyframes, and multi-panel visualizations.

    Args:
        preset_name: One of the 5 rhythmic presets
        keyframe_count: Number of keyframes to extract (default: 4)
        style_modifier: Optional style prefix for all prompts

    Returns:
        Keyframes with step index, state, prompt, and vocabulary.
    """
    if preset_name not in RHYTHMIC_PRESETS:
        return json.dumps({
            "error": f"Unknown preset: {preset_name}",
            "available": list(RHYTHMIC_PRESETS.keys()),
        })

    preset = RHYTHMIC_PRESETS[preset_name]
    state_a = CANONICAL_STATES[preset["state_a"]]
    state_b = CANONICAL_STATES[preset["state_b"]]
    period = preset["period"]
    pattern = preset["pattern"]

    keyframes = []
    for ki in range(keyframe_count):
        step = round(ki * period / keyframe_count)
        t = step / period
        raw_t = t * 2 if t <= 0.5 else 2 * (1 - t)
        state = _interpolate_states(state_a, state_b, raw_t, pattern)
        state_rounded = {p: round(v, 4) for p, v in state.items()}

        vtype_id, _ = _nearest_visual_type(state)
        vtype = VISUAL_TYPES[vtype_id]
        vocab = _select_vocabulary(state)

        parts = []
        if style_modifier:
            parts.append(style_modifier)
        parts.extend(vtype["keywords"][:3])
        for cat, terms in vocab.items():
            if terms:
                parts.append(terms[1] if len(terms) > 1 else terms[0])

        keyframes.append({
            "keyframe": ki,
            "step": step,
            "phase": round(t, 4),
            "state": state_rounded,
            "visual_type": vtype_id,
            "prompt": ", ".join(parts),
        })

    return json.dumps({
        "preset": preset_name,
        "period": period,
        "pattern": pattern,
        "keyframe_count": keyframe_count,
        "keyframes": keyframes,
    }, indent=2)


# ============================================================================
# Layer 2: Attractor Preset Visualization (Phase 2.7 — Tier 4D Integration)
# ============================================================================


@mcp.tool(
    name="list_surface_attractor_presets",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def list_surface_attractor_presets() -> str:
    """List all available surface attractor presets for visualization.

    Phase 2.7 Tool: Shows discovered and curated attractor configurations
    available for prompt generation.

    Returns:
        Dict with preset names, descriptions, basin sizes, and classifications.

    Cost: 0 tokens
    """
    result = {}
    for preset_id, preset in ATTRACTOR_PRESETS.items():
        result[preset_id] = {
            "name": preset["name"],
            "description": preset["description"],
            "basin_size": preset["basin_size"],
            "classification": preset["classification"],
            "source_domains": preset["source_domains"],
        }
    return json.dumps(result, indent=2)


@mcp.tool(
    name="generate_surface_attractor_prompt",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def generate_surface_attractor_prompt(
    attractor_id: str = "",
    custom_state: Optional[Dict[str, float]] = None,
    mode: str = "composite",
    style_modifier: str = "",
    keyframe_count: int = 4,
) -> str:
    """Generate image generation prompt from attractor state or custom coordinates.

    Phase 2.7 Tool: Translates mathematical attractor coordinates into
    visual prompts suitable for image generation (ComfyUI, Stable Diffusion,
    DALL-E, etc.).

    Modes:
        composite:  Single blended prompt from attractor state
        split_view: Separate prompt per vocabulary category
        sequence:   Multiple keyframe prompts cycling through nearest
                    rhythmic preset trajectory

    Args:
        attractor_id: Preset attractor name (period_30, period_19, etc.)
            Use "" with custom_state for arbitrary coordinates.
        custom_state: Optional custom parameter coordinates dict.
            Overrides attractor_id if provided.
        mode: "composite" | "split_view" | "sequence"
        style_modifier: Optional prefix ("photorealistic", "oil painting", etc.)
        keyframe_count: Number of keyframes for sequence mode (default: 4)

    Returns:
        Dict with prompt(s), vocabulary details, and attractor metadata.

    Cost: 0 tokens (Layer 2 deterministic)

    Available attractor presets:
        period_30: Universal Sync (11.6% basin, LCM)
        period_29: Emergent Resonance (8.4% basin, LCM)
        period_19: Gap Flow (7.4% basin, novel)
        period_28: Composite Beat (2.4% basin, novel)
        period_60: Harmonic Hub (4.0% basin, harmonic)
        bifurcation_edge: Cusp threshold (curated)
        organic_complexity: Emergence bloom (curated)

    Example:
        >>> generate_surface_attractor_prompt("period_28", mode="composite")
        {
            "prompt": "satin semi-gloss directional highlights, ...",
            "attractor": {"name": "Period 28 — Composite Beat", ...},
            "vocabulary": {"nearest_type": "translucent_diffuse", ...}
        }
    """
    # Resolve state
    if custom_state is not None:
        state = custom_state
        attractor_meta = {
            "name": "Custom State",
            "description": "User-provided parameter coordinates",
            "basin_size": None,
            "classification": "custom",
        }
    elif attractor_id and attractor_id in ATTRACTOR_PRESETS:
        preset = ATTRACTOR_PRESETS[attractor_id]
        state = preset["state"]
        attractor_meta = {
            "name": preset["name"],
            "description": preset["description"],
            "basin_size": preset["basin_size"],
            "classification": preset["classification"],
            "source_domains": preset["source_domains"],
        }
    else:
        return json.dumps({
            "error": f"Unknown attractor: {attractor_id}" if attractor_id else "Provide attractor_id or custom_state",
            "available_presets": list(ATTRACTOR_PRESETS.keys()),
        })

    # Validate state keys
    missing = [p for p in PARAMETER_NAMES if p not in state]
    if missing:
        return json.dumps({"error": f"Missing parameters: {missing}", "required": PARAMETER_NAMES})

    # Extract vocabulary from state
    vtype_id, vtype_dist = _nearest_visual_type(state)
    vtype = VISUAL_TYPES[vtype_id]
    vocab = _select_vocabulary(state)

    # ── Composite mode: single blended prompt ─────────────────────────
    if mode == "composite":
        parts = []
        if style_modifier:
            parts.append(style_modifier)

        # Primary keywords from nearest visual type
        parts.extend(vtype["keywords"][:3])

        # One term from each vocabulary category (pick the primary match)
        for cat, terms in vocab.items():
            if terms:
                parts.append(terms[1] if len(terms) > 1 else terms[0])

        # Optical properties as explicit geometric spec
        optical = vtype["optical"]
        parts.append(f"{optical['finish']} finish, {optical['scatter']} light scatter")

        prompt = ", ".join(parts)

        return json.dumps({
            "mode": "composite",
            "prompt": prompt,
            "attractor": attractor_meta,
            "vocabulary": {
                "nearest_type": vtype_id,
                "distance": round(vtype_dist, 4),
                "keywords": vtype["keywords"],
                "optical": vtype["optical"],
            },
            "state": {p: round(v, 4) for p, v in state.items()},
        }, indent=2)

    # ── Split-view mode: separate prompt per category ─────────────────
    elif mode == "split_view":
        panels = {}
        for cat, terms in vocab.items():
            panel_parts = []
            if style_modifier:
                panel_parts.append(style_modifier)
            panel_parts.extend(terms)
            panels[cat] = ", ".join(panel_parts)

        return json.dumps({
            "mode": "split_view",
            "panels": panels,
            "attractor": attractor_meta,
            "vocabulary": {
                "nearest_type": vtype_id,
                "distance": round(vtype_dist, 4),
                "optical": vtype["optical"],
            },
            "state": {p: round(v, 4) for p, v in state.items()},
        }, indent=2)

    # ── Sequence mode: keyframes from nearest rhythmic preset ─────────
    elif mode == "sequence":
        # Find the rhythmic preset whose period best matches this attractor
        best_preset_name = None
        best_period_diff = float("inf")

        if attractor_id and attractor_id in ATTRACTOR_PRESETS:
            target_period = int(attractor_id.split("_")[-1]) if attractor_id.startswith("period_") else None
        else:
            target_period = None

        for pname, pdata in RHYTHMIC_PRESETS.items():
            if target_period is not None:
                diff = abs(pdata["period"] - target_period)
            else:
                # Fall back to nearest preset by state distance
                pa = CANONICAL_STATES[pdata["state_a"]]
                pb = CANONICAL_STATES[pdata["state_b"]]
                midpoint = {p: (pa[p] + pb[p]) / 2.0 for p in PARAMETER_NAMES}
                diff = _euclidean_distance(state, midpoint) * 100  # scale for comparison
            if diff < best_period_diff:
                best_period_diff = diff
                best_preset_name = pname

        # Generate keyframes from that preset
        preset = RHYTHMIC_PRESETS[best_preset_name]
        state_a = CANONICAL_STATES[preset["state_a"]]
        state_b = CANONICAL_STATES[preset["state_b"]]
        period = preset["period"]
        pattern = preset["pattern"]

        keyframes = []
        for ki in range(keyframe_count):
            step = round(ki * period / keyframe_count)
            t = step / period
            raw_t = t * 2 if t <= 0.5 else 2 * (1 - t)
            kf_state = _interpolate_states(state_a, state_b, raw_t, pattern)

            kf_vtype_id, _ = _nearest_visual_type(kf_state)
            kf_vtype = VISUAL_TYPES[kf_vtype_id]
            kf_vocab = _select_vocabulary(kf_state)

            parts = []
            if style_modifier:
                parts.append(style_modifier)
            parts.extend(kf_vtype["keywords"][:3])
            for cat, terms in kf_vocab.items():
                if terms:
                    parts.append(terms[1] if len(terms) > 1 else terms[0])

            keyframes.append({
                "keyframe": ki,
                "step": step,
                "phase": round(t, 4),
                "state": {p: round(v, 4) for p, v in kf_state.items()},
                "visual_type": kf_vtype_id,
                "prompt": ", ".join(parts),
            })

        return json.dumps({
            "mode": "sequence",
            "preset_used": best_preset_name,
            "period": period,
            "pattern": pattern,
            "keyframe_count": keyframe_count,
            "keyframes": keyframes,
            "attractor": attractor_meta,
        }, indent=2)

    else:
        return json.dumps({"error": f"Unknown mode: {mode}. Use 'composite', 'split_view', or 'sequence'"})


# ============================================================================
# Domain Registry Helper (Tier 4D Integration)
# ============================================================================

def get_domain_registry_config() -> dict:
    """Return configuration for domain_registry.py integration.

    Call this to get everything needed to register surface_design
    in the emergent attractor discovery system.

    Returns:
        Dict with domain_id, parameter_names, state_coordinates,
        preset_configs, and vocabulary — ready for DomainConfig().
    """
    preset_configs = {}
    for pname, pdata in RHYTHMIC_PRESETS.items():
        preset_configs[pname] = {
            "name": pname,
            "period": pdata["period"],
            "state_a_id": pdata["state_a"],
            "state_b_id": pdata["state_b"],
            "pattern": pdata["pattern"],
            "description": pdata["description"],
        }

    # Flatten vocabulary for registry
    flat_vocab = {}
    for cat, terms in VISUAL_VOCABULARY.items():
        flat_vocab[cat] = terms

    return {
        "domain_id": "surface_design",
        "display_name": "Surface Design Aesthetics",
        "description": (
            "Material finish morphospace from mirror-smooth automotive lacquer "
            "to densely spiked organic seedcoats"
        ),
        "mcp_server": "surface-design-aesthetics",
        "parameter_names": list(PARAMETER_NAMES),
        "state_coordinates": dict(CANONICAL_STATES),
        "presets": preset_configs,
        "vocabulary": flat_vocab,
        "periods": sorted(set(p["period"] for p in RHYTHMIC_PRESETS.values())),
        "attractor_presets": {
            k: {"state": v["state"], "basin_size": v["basin_size"], "classification": v["classification"]}
            for k, v in ATTRACTOR_PRESETS.items()
        },
    }


# ============================================================================
# Layer 2: Server Info
# ============================================================================

@mcp.tool(
    name="get_surface_server_info",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def get_surface_server_info() -> str:
    """Get information about the Surface Design Aesthetics MCP server.

    Returns server metadata, capabilities, and phase status.
    """
    return json.dumps({
        "name": "Surface Design Aesthetics MCP",
        "version": "2.0.0-phase2.7+tier4d",
        "description": (
            "Material finish morphospace spanning the full range of surface treatments "
            "from mirror-smooth automotive lacquer to densely spiked organic seedcoats. "
            "Includes Phase 2.6 rhythmic presets, Phase 2.7 attractor visualization, "
            "and Tier 4D emergent attractor integration."
        ),
        "parameter_space": {
            "parameters": PARAMETER_NAMES,
            "bounds": PARAMETER_BOUNDS,
            "dimensionality": DIMENSIONALITY,
        },
        "canonical_states": list(CANONICAL_STATES.keys()),
        "visual_types": list(VISUAL_TYPES.keys()),
        "rhythmic_presets": {
            name: {"period": p["period"], "pattern": p["pattern"]}
            for name, p in RHYTHMIC_PRESETS.items()
        },
        "attractor_presets": {
            aid: {
                "name": a["name"],
                "basin_size": a["basin_size"],
                "classification": a["classification"],
            }
            for aid, a in ATTRACTOR_PRESETS.items()
        },
        "vocabulary_categories": list(VISUAL_VOCABULARY.keys()),
        "total_vocabulary_terms": sum(len(v) for v in VISUAL_VOCABULARY.values()),
        "capabilities": {
            "layer_1_taxonomy": [
                "get_surface_types — list all canonical surfaces",
                "get_surface_specifications — complete visual specs",
            ],
            "layer_2_deterministic": [
                "map_surface_parameters — parameter mapping with intensity/emphasis",
                "compute_surface_distance — distance between surfaces",
                "compute_surface_trajectory — smooth interpolation path",
                "list_surface_rhythmic_presets — preset catalog",
                "apply_surface_rhythmic_preset — curated rhythmic patterns",
                "generate_surface_rhythmic_sequence — custom oscillation",
                "extract_surface_visual_vocabulary — coordinate→keyword mapping",
                "generate_surface_prompt — surface→image prompt",
                "generate_surface_sequence_prompts — keyframe prompts from presets",
                "list_surface_attractor_presets — Tier 4D attractor catalog",
                "generate_surface_attractor_prompt — attractor→image prompt (composite/split/sequence)",
                "decompose_surface_from_description — text→5D coordinates (inverse pipeline)",
            ],
        },
        "phase_2_7_enhancements": {
            "attractor_visualization": True,
            "supported_modes": ["composite", "split_view", "sequence"],
            "attractor_count": len(ATTRACTOR_PRESETS),
            "tier_4d_integration": True,
            "domain_registry_ready": True,
        },
        "compatible_servers": [
            "aesthetic-dynamics-core — trajectory integration, attractor discovery",
            "catastrophe-morph-mcp — cross-domain composition (material ↔ geometry)",
            "diatom-morph-mcp — microscopic surface structure overlay",
            "reflective-surfaces-mcp — specialized reflection optics",
            "composition-graph-mcp — central orchestrator for multi-domain composition",
        ],
        "cost_profile": {
            "layer_1": "0 tokens (pure lookup)",
            "layer_2": "0 tokens (deterministic computation + prompt generation)",
        },
        "domain_periods": sorted(set(p["period"] for p in RHYTHMIC_PRESETS.values())),
    }, indent=2)


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    mcp.run()
