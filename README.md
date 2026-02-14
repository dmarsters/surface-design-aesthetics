# Surface Design Aesthetics MCP Server

Visual aesthetics derived from material science and surface treatment design. Parametrizes the full range of surface finishes — from mirror-smooth automotive lacquer to densely spiked organic seedcoats — as a navigable 5D morphospace.

## Why Surface Design?

Surface design is the discipline that determines how light interacts with objects at the material level. Unlike the Reflective Surfaces domain (narrowly scoped to mirror/glass/metal optics), this domain covers the **full material taxonomy**: matte, absorbent, textured, organic, soft, rigid, translucent, and synthetic surfaces.

The domain was motivated by editorial and fashion imagery that deploys 6-7 distinct surface treatments simultaneously — lacquered hair, beaded textiles, matte ceramics, waxy botanicals, spiky seed coats, woven fibers — and the need to parametrize those choices for text-to-image generation.

## Parameter Space

5D normalized continuous space `[0.0, 1.0]`:

| Parameter | Low (0.0) | High (1.0) |
|---|---|---|
| `specularity` | Fully matte / absorbent | Perfect mirror |
| `micro_texture_density` | Glass-smooth | Densely packed micro-features |
| `material_hardness` | Soft / pliable / draped | Rigid / crystalline / brittle |
| `organic_synthetic_ratio` | Purely manufactured | Purely biological / natural |
| `surface_pattern_scale` | No pattern / uniform | Large macro-repeat pattern |

## Canonical States

9 surface treatment archetypes spanning the morphospace:

| State | Specularity | Texture | Hardness | Organic | Pattern |
|---|---|---|---|---|---|
| `automotive_lacquer` | 0.95 | 0.02 | 0.85 | 0.00 | 0.05 |
| `beaded_textile` | 0.45 | 0.90 | 0.35 | 0.20 | 0.40 |
| `matte_ceramic` | 0.10 | 0.08 | 0.90 | 0.15 | 0.00 |
| `waxy_botanical` | 0.55 | 0.15 | 0.40 | 0.95 | 0.30 |
| `spiky_seedcoat` | 0.15 | 0.95 | 0.75 | 1.00 | 0.55 |
| `polished_stone` | 0.80 | 0.05 | 0.95 | 0.70 | 0.65 |
| `woven_fiber` | 0.10 | 0.70 | 0.15 | 0.80 | 0.75 |
| `liquid_chrome` | 1.00 | 0.00 | 0.70 | 0.00 | 0.00 |
| `frosted_glass` | 0.25 | 0.50 | 0.85 | 0.05 | 0.10 |

## Rhythmic Presets

5 oscillation patterns for temporal composition:

| Preset | Period | Pattern | Transition |
|---|---|---|---|
| `sheen_oscillation` | 15 | sinusoidal | matte ceramic ↔ automotive lacquer |
| `texture_accretion` | 19 | triangular | liquid chrome ↔ spiky seedcoat |
| `material_softening` | 21 | sinusoidal | polished stone ↔ woven fiber |
| `nature_synthesis` | 24 | sinusoidal | automotive lacquer ↔ waxy botanical |
| `full_palette_morph` | 30 | sinusoidal | frosted glass ↔ beaded textile |

### Period Strategy

- **15**: Syncs with nuclear `energy_pulse`, reflective `distortion_wave`, catastrophe `symmetry_pulse`
- **19**: Prime gap-filler — complex irrational beats with all neighbors (LCM(19,15)=285, LCM(19,24)=456)
- **21**: Beats with microscopy/reflective period-20 presets (LCM(21,20)=420)
- **24**: Harmonic triad with microscopy `focus_sweep`, brassiere `editorial_transition` (2×12)
- **30**: Major LCM hub for full-system synchronization

## Tools

### Layer 1 — Taxonomy (0 tokens)

| Tool | Description |
|---|---|
| `get_surface_types` | List all 9 canonical surface types |
| `get_surface_specifications` | Complete visual specs for a surface type |

### Layer 2 — Deterministic Computation (0 tokens)

| Tool | Description |
|---|---|
| `map_surface_parameters` | Parameter mapping with intensity/emphasis control |
| `compute_surface_distance` | Distance between two surface types |
| `compute_surface_trajectory` | Smooth interpolation path between surfaces |
| `list_surface_rhythmic_presets` | Preset catalog |
| `apply_surface_rhythmic_preset` | Curated rhythmic pattern generation |
| `generate_surface_rhythmic_sequence` | Custom oscillation between any two surfaces |
| `extract_surface_visual_vocabulary` | 5D coordinates → image-gen keywords |
| `generate_surface_prompt` | Surface state → composite or split-view prompt |
| `generate_surface_sequence_prompts` | Keyframe prompts from rhythmic presets |

## Visual Vocabulary

62 concrete image-generation-ready terms across 8 categories:

- **finish** — specularity descriptors (clearcoat, satin, eggshell, chalk matte, pearlescent)
- **micro_texture** — surface roughness (glass-smooth, stipple, beaded, studded, bristle, pebbled)
- **material_character** — hardness/pliability (porcelain, polymer, stoneware, draped fabric, silicone)
- **organic_surface** — natural materials (waxy cuticle, bark, seed pod armor, petal papillae, chitin)
- **synthetic_surface** — manufactured materials (automotive paint, chrome plate, carbon fiber, concrete)
- **pattern_scale** — repeat structure (uniform, micro-pattern, mosaic, motif, fractal)
- **light_interaction** — optical behavior (specular, diffuse, subsurface scatter, retroreflective)
- **color_palette** — material-native colors (raw material, industrial, automotive candy, botanical, mineral)

## Installation

```bash
pip install surface-design-aesthetics
```

## Running

```bash
# Local (stdio)
python surface_design_server.py

# Remote (streamable HTTP)
fastmcp run surface_design_server.py

# Deploy to FastMCP cloud
fastmcp deploy surface_design_server.py --name surface-design-aesthetics
```

## Compatible Servers

- **aesthetic-dynamics-core** — Trajectory integration, attractor basin discovery
- **catastrophe-morph-mcp** — Cross-domain composition (material ↔ geometry)
- **diatom-morph-mcp** — Microscopic surface structure overlay
- **reflective-surfaces-mcp** — Specialized reflection optics (narrower but deeper)

## Domain Registry Integration

Register in your `domain_registry.py` `initialize_registry()`:

```python
from surface_design_domain import register_surface_design_domain
register_surface_design_domain()
```

The `mcp_server` field points to `"surface-design-aesthetics"`, matching the FastMCP deployment name.

## License

MIT
