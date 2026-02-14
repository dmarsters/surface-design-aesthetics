"""
Surface Design Aesthetics MCP Server
======================================

Visual aesthetics derived from material science and surface treatment design.

Covers the full range of surface treatments from mirror-smooth automotive lacquer
to densely spiked organic seedcoats. Parametrizes specularity, micro-texture,
material hardness, organic/synthetic character, and pattern scale.

Layer Architecture:
    Layer 1 (Taxonomy):     Pure lookup, 0 tokens
    Layer 2 (Deterministic): Parameter mapping, distance, trajectory, rhythm, vocabulary — 0 tokens
    Layer 3 (Synthesis):     Claude-assisted visualization context — ~100-200 tokens

Compatible with:
    - aesthetic-dynamics-core: Trajectory integration, attractor discovery
    - catastrophe-morph-mcp: Cross-domain composition (material ↔ geometry)
    - diatom-morph-mcp: Microscopic surface structure overlay

Deployment:
    fastmcp run surface_design_server.py
    # or
    fastmcp deploy surface_design_server.py --name surface-design-aesthetics
"""

import json
import math
from typing import Dict, List, Optional, Any
from mcp.server.fastmcp import FastMCP

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
    },
    "matte_mineral": {
        "center": {"specularity": 0.10, "micro_texture_density": 0.10, "material_hardness": 0.90,
                    "organic_synthetic_ratio": 0.20, "surface_pattern_scale": 0.10},
        "keywords": ["chalk matte fully absorbent surface", "rigid porcelain brittle edges",
                      "sandblasted micro-roughness", "powder-coated matte finish", "cast concrete aggregate"],
        "optical": {"finish": "matte", "scatter": "full_diffuse", "transparency": "opaque"},
    },
    "textured_embellished": {
        "center": {"specularity": 0.40, "micro_texture_density": 0.85, "material_hardness": 0.35,
                    "organic_synthetic_ratio": 0.25, "surface_pattern_scale": 0.50},
        "keywords": ["raised dot matrix beaded surface", "densely studded micro-protrusions",
                      "small-scale repeat tile mosaic chainmail", "pebbled grain dimpled surface",
                      "hammered metal irregular concavity"],
        "optical": {"finish": "semi-gloss", "scatter": "micro_faceted", "transparency": "opaque"},
    },
    "organic_botanical": {
        "center": {"specularity": 0.40, "micro_texture_density": 0.30, "material_hardness": 0.45,
                    "organic_synthetic_ratio": 0.95, "surface_pattern_scale": 0.35},
        "keywords": ["waxy leaf cuticle hydrophobic beading", "petal velvet papillae",
                      "mushroom cap hygroscopic sheen", "bark deep fissure channels",
                      "botanical palette chlorophyll green pollen gold"],
        "optical": {"finish": "waxy_sheen", "scatter": "subsurface", "transparency": "translucent_edges"},
    },
    "spiny_armor": {
        "center": {"specularity": 0.15, "micro_texture_density": 0.95, "material_hardness": 0.80,
                    "organic_synthetic_ratio": 0.90, "surface_pattern_scale": 0.55},
        "keywords": ["seed pod armor conical spike protrusions", "insect chitin layered structural color",
                      "coral skeleton porous calcium lattice", "tightly packed bristle array",
                      "eggshell calcium carbonate micro-pore"],
        "optical": {"finish": "matte_rough", "scatter": "shadow_field", "transparency": "opaque"},
    },
    "soft_woven": {
        "center": {"specularity": 0.10, "micro_texture_density": 0.65, "material_hardness": 0.15,
                    "organic_synthetic_ratio": 0.75, "surface_pattern_scale": 0.70},
        "keywords": ["supple draped fabric following gravity", "stiff architectural felt",
                      "fibrous wood grain directional strength", "carbon fiber weave under clear resin",
                      "fractal self-similar pattern multiple zoom levels"],
        "optical": {"finish": "matte_soft", "scatter": "fiber_diffuse", "transparency": "opaque"},
    },
    "translucent_diffuse": {
        "center": {"specularity": 0.30, "micro_texture_density": 0.40, "material_hardness": 0.80,
                    "organic_synthetic_ratio": 0.10, "surface_pattern_scale": 0.10},
        "keywords": ["frosted glass translucent diffusion", "subsurface scattering internal glow",
                      "blown glass internal bubble inclusions", "translucent edge-lit glow",
                      "eggshell finish absorbing light faint sheen"],
        "optical": {"finish": "frosted", "scatter": "volume", "transparency": "translucent"},
    },
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
        "version": "1.0.0-phase2.7",
        "description": (
            "Material finish morphospace spanning the full range of surface treatments "
            "from mirror-smooth automotive lacquer to densely spiked organic seedcoats"
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
            ],
        },
        "compatible_servers": [
            "aesthetic-dynamics-core — trajectory integration, attractor discovery",
            "catastrophe-morph-mcp — cross-domain composition (material ↔ geometry)",
            "diatom-morph-mcp — microscopic surface structure overlay",
            "reflective-surfaces-mcp — specialized reflection optics",
        ],
        "cost_profile": {
            "layer_1": "0 tokens (pure lookup)",
            "layer_2": "0 tokens (deterministic computation + prompt generation)",
        },
    }, indent=2)


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    mcp.run()
