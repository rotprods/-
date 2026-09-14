# SYLVA PRIME — BIOLOGICAL REALISM REFERENCE PACK R14

**Purpose:** translate real plant/tree biomechanics, wound response and root interaction into physically credible 3D design principles for SYLVA PRIME.  
**Status:** `REFERENCE / DESIGN TRANSLATION`, not universe canon and not permission to copy figures or authored visual designs.  
**Rule:** extract mechanisms and constraints; create original EXOVANT morphology.

---

## 0. Critical scientific boundary

SYLVA PRIME canon contains a living information network with local delay and contextual responses. **Do not claim that real forests are scientifically known to operate like Sylva.**

Current scientific literature supports:
- mechanical/hydraulic adaptation of woody tissues;
- physical root grafts and some resource/water exchange;
- fungi connecting plant roots in common mycorrhizal networks;
- experimental changes in plant defence when networked plants are disturbed in some systems.

It does **not** justify popular claims that mature trees generally and intentionally send complex warnings/resources to preferred relatives through a forest-wide conscious network. Critical literature explicitly warns about overinterpretation and citation bias.

Therefore:

> **Real biomechanics grounds Sylva's material realism. Sylva's deliberate information ecology remains original science fiction canon.**

---

# 1. ROOT ANCHORAGE / LOAD PATHS

## SOURCE R-BIO-001

**Source:** Niklas, K.J. et al., “A general review of the biomechanics of root anchorage”, *Journal of Experimental Botany* 70(14), 2019. DOI: `10.1093/jxb/ery451`.  
Reference page: `https://academic.oup.com/jxb/article/70/14/3439/5304217`

**Purpose:** root-system mechanical anchorage.

**Observation:** roots resist bending/twisting and anchorage failure under gravity/wind loads; stability depends on how root systems distribute and adapt to mechanical forces, not simply root volume.

**Design translation:**
- major Sylva roots must visibly oppose plausible load directions;
- a large elevated mass needs a root fan/buttress system with understandable moment resistance;
- root branches should widen/flatten/orient where bending moments demand it;
- do not distribute equal-thickness roots radially by decorative symmetry.

**3D QA:** from a grayscale structural view, a technical artist should be able to sketch the dominant force path from supported mass to terrain.

**Provenance/license handling:** peer-reviewed reference; use principles only; do not copy article figures.

---

# 2. MECHANICAL–HYDRAULIC TRADE-OFF

## SOURCE R-BIO-002

**Source:** “Interrelations between hydraulic and mechanical stress adaptations in woody plants”, available via PMC (`PMC2634430`).  
Reference: `https://pmc.ncbi.nlm.nih.gov/articles/PMC2634430/`

**Purpose:** connect load-bearing form to internal material anatomy.

**Observation:** in studied buttressed tropical trees, tissue nearer highly loaded regions was stronger/stiffer; distal roots became less mechanically reinforced while conductivity increased. Mechanical and hydraulic functions can trade off within the same woody structure.

**Design translation:**

### Proximal / high-load Sylva root
- denser-looking fiber organization;
- thicker structural section;
- stronger buttress/elliptical geometry;
- fewer visually dominant hydraulic channels;
- compressed/polished contact surfaces where load transfers.

### Distal / low-load transport root
- narrower section;
- relatively more visible vascular/channel organization;
- greater curvature tolerance;
- less massive buttressing.

**Material implication:** one “root bark” shader across every radius is physically weak art direction. Material masks/microstructure should vary by functional zone.

**Procedural implication:** Geometry Nodes/provider generators should expose at least:
- load/proximity class;
- structural aspect ratio;
- fiber/ridge direction;
- channel-density mask or material parameter.

---

# 3. REACTION WOOD / ACTIVE POSTURE CONTROL

## SOURCE R-BIO-003

**Source:** Alméras et al., “Critical review on the mechanisms of maturation stress generation in trees”, Royal Society / PMC `PMC5046956`, 2016.  
Reference: `https://pmc.ncbi.nlm.nih.gov/articles/PMC5046956/`

**Observation:** trees generate asymmetric maturation stresses and specialized reaction wood to control posture. Angiosperms and gymnosperms use different tension/compression mechanisms; the key production lesson is **asymmetric adaptation to mechanical need**.

## SOURCE R-BIO-004

**Source:** “Environmental–biomechanical reciprocity and the evolution of plant material properties”, *Journal of Experimental Botany* 73(4), 2022.  
Reference: `https://academic.oup.com/jxb/article/73/4/1067/6364876`

**Observation:** reaction wood can produce eccentric/asymmetric cross-sections and altered cell/material organization in response to gravity, wind, growth orientation and other stimuli.

## SOURCE R-BIO-005

**Source:** “Structural Characteristics of Reaction Tissue in Plants”, PMC `PMC10146549`, 2023.  
Reference: `https://pmc.ncbi.nlm.nih.gov/articles/PMC10146549/`

**Design translation:**
- leaning or heavily loaded Sylva roots should not preserve perfectly circular cross-sections;
- high-stress curvature can produce eccentric thickening;
- visible fiber/ridge direction should correlate with corrective load;
- repaired/reoriented growth can retain an old axis plus newer compensating mass.

**Anti-CGI rule:** procedural roots with constant circular bevel profiles are acceptable as macro blockout only, not final hero roots.

**3D implementation candidate:** final root modules can use an elliptical profile whose major/minor axes and centroid offset are parameters driven by a stress-side vector rather than random noise.

---

# 4. BUTTRESS / FLYING-BUTTRESS MORPHOLOGY

## SOURCE R-BIO-006

**Source:** “Root biomechanics in *Rhizophora mangle*: anatomy, morphology and ecology of mangrove’s flying buttresses”, PMC `PMC4373286`, 2015.  
Reference: `https://pmc.ncbi.nlm.nih.gov/articles/PMC4373286/`

**Observation:** mangrove rhizophores can behave as flying-buttress-like supports; measured buttress morphology scaled with tree dimensions/crown area and showed distinct mechanical resistance.

**Design translation for Sylva:**
- VESPER/forest-city buttresses should scale with the mass they support;
- a high narrow tower requires longer/higher or more numerous support paths, not decorative roots of fixed size;
- buttresses should converge into meaningful compression zones;
- attachment locations should correspond to structural nodes rather than evenly spaced ring decoration.

**Current implication:** r13 VESPER buttresses are diagnostic; final context agent must perform a support/mass review before hero polish.

---

# 5. NATURAL ROOT GRAFTING / RESOURCE CONNECTION

## SOURCE R-BIO-007

**Source:** Vovides et al., “Root grafts matter for inter-tree water exchange…”, *Annals of Botany* 130(3), 2022; PMC `PMC9486923`.  
Reference: `https://pmc.ncbi.nlm.nih.gov/articles/PMC9486923/`

**Observation:** functional root grafts can permit water/resource translocation between connected trees; the reviewed literature includes direct tracing evidence, while ecological consequences remain context-dependent.

## SOURCE R-BIO-008

**Source:** Lev-Yadun, “Why should trees have natural root grafts?”, *Tree Physiology* 31(6), 2011. DOI `10.1093/treephys/tpr061`.  
Reference: `https://academic.oup.com/treephys/article-abstract/31/6/575/1657428`

**Observation:** natural root grafts occur across many species and have been discussed in relation to resource transfer and anchorage, among other effects.

## SOURCE R-BIO-009

**Source:** “Insights Into Plant Surgery: An Overview of the Multiple Grafting Techniques for *Arabidopsis thaliana*”, PMC `PMC7758207`, 2020.  
Reference: `https://pmc.ncbi.nlm.nih.gov/articles/PMC7758207/`

**Observation:** natural root grafts can form via contact/fusion, distinct from human grafts based on cutting/deep wounds; compatible vascular connection matters.

**Design translation:**

### Natural network junction
- surfaces meet through broad biological fusion;
- external contour should show gradual tissue continuity;
- old seam can remain readable but should not look bolted.

### Human graft junction
- intentional incision/contact preparation may be visible;
- clamp/support hardware carries load while tissue adapts;
- wound/callus boundary develops around intervention;
- replaceable human components remain distinguishable.

This supports the art-direction distinction between **network-native fusion** and **colonial graft hardware**.

---

# 6. WOUND RESPONSE / CALLUS / COMPARTMENTALIZATION

## SOURCE R-BIO-010

**Source:** Morris/Smith CODIT commentary, *Annals of Botany* 125(5), 2020; PMC `PMC7182581`.  
Reference: `https://pmc.ncbi.nlm.nih.gov/articles/PMC7182581/`

**Observation:** tree responses to injury include compartmentalization boundaries that limit loss of function and spread of infection; new tissue after injury can remain anatomically distinct from pre-injury wood.

## SOURCE R-BIO-011

**Source:** “The Parenchyma of Secondary Xylem and Its Critical Role in Tree Defense…”, PMC `PMC5101214`, 2016.  
Reference: `https://pmc.ncbi.nlm.nih.gov/articles/PMC5101214/`

**Observation:** callus/wound wood and chemically/anatomically altered barrier zones can form after injury; wound depth and tissue state affect the response.

## SOURCE R-BIO-012

**Source:** “Developmental Stages and Fine Structure of Surface Callus Formed after Debarking of Living Lime Trees”, PMC `PMC4233843`.  
Reference: `https://pmc.ncbi.nlm.nih.gov/articles/PMC4233843/`

**Observation:** studied wound closure progresses through callus proliferation, wound-periderm differentiation and later development of a wound cambium producing new vascular tissue.

## SOURCE R-BIO-013

**Source:** “Duration and extension of anatomical changes in wood structure after cambial injury”, *Journal of Experimental Botany* 63(8).  
Reference: `https://academic.oup.com/jxb/article/63/8/3271/733293`

**Observation:** restoring mechanical strength/safety after wounding can involve increased callus mass and altered tissue anatomy, with trade-offs in transport/growth.

**Design translation:** Sylva wounds need **depth and chronology**.

### Fresh injury
- exposed disrupted fiber direction;
- local fluids/residue if species physiology supports it;
- no instant smooth rim.

### Early response
- irregular proliferative tissue;
- edge swelling;
- protective boundary forming.

### Mature repair
- raised callus lip;
- altered growth ring/fiber direction;
- closed or partially enclosed scar;
- local structural thickening;
- potentially different surface material/roughness from original tissue.

### Repeated human interface
- older callus mass can engulf/support previous hardware;
- replacement clamp may sit outside older scar geometry;
- repair chronology should be readable in layers.

**Anti-CGI rule:** never represent old damage only with a flat dark decal plus scratch normal.

---

# 7. COMMON MYCORRHIZAL NETWORKS — EVIDENCE CAUTION

## SOURCE R-BIO-014

**Source:** Karst, Jones & Hoeksema, “Positive citation bias and overinterpreted results lead to misinformation on common mycorrhizal networks in forests”, *Nature Ecology & Evolution* 7, 2023.  
Reference: `https://www.nature.com/articles/s41559-023-01986-1`

**Observation:** the authors argue that several widespread popular claims about forest common-mycorrhizal networks are insufficiently supported and that citation bias has amplified claims beyond evidence.

## SOURCE R-BIO-015

**Source:** “The evolution of signaling and monitoring in plant–fungal networks”, PMC `PMC7617349`.  
Reference: `https://pmc.ncbi.nlm.nih.gov/articles/PMC7617349/`

**Observation:** some experiments show connected plants changing defence after another plant is attacked, but theoretical work finds intentional plant warning signals hard to stabilize evolutionarily; cues or fungal monitoring/signaling are alternative explanations.

## SOURCE R-BIO-016

**Source:** “Common Mycorrhizae Network: A Review of the Theories and Mechanisms Behind Underground Interactions”, PMC `PMC10512311` / Frontiers.  
Reference: `https://pmc.ncbi.nlm.nih.gov/articles/PMC10512311/`

**Observation:** CMNs can physically connect plants, but quantifying transfer and separating direct-network effects from indirect soil/microbial pathways is difficult and debated.

**EXOVANT rule:**

Do **not** write production docs saying:
- “real trees talk like the internet”;
- “mother trees are scientifically proven to warn children”;
- “mycorrhiza proves Sylva”.

Instead:

> Real fungal/root networks inspire the existence of physical interconnections; EXOVANT fiction supplies the sophisticated information-processing rules.

This preserves scientific credibility while allowing the canon to remain imaginative.

---

# 8. 3D MORPHOLOGY COMPILER

Use this table to convert function into modeled form.

| Physical role | Macro geometry | Meso geometry | Micro/material cue |
|---|---|---|---|
| high mechanical load | wider/elliptical buttress, shorter load path | aligned ridges, compressed junction | dense fiber, contact polish |
| corrective/reaction growth | eccentric thickening | asymmetric layers | directional fiber/material shift |
| hydraulic/transport emphasis | narrower distal root | channel organization | less massive structural fiber cue |
| natural root graft | broad fused junction | intergrown seam/callus | tissue continuity |
| human graft | prepared contact + brace/clamp | fasteners/straps + callus interaction | tool marks, repair chronology |
| fresh wound | broken/recessed section | torn fibers | wet/residue variation if justified |
| mature wound | raised/encircling callus | barrier/woundwood layers | roughness/color/material transition |
| repeated traffic | compressed crown | rounded/expanded callus edge | directional polish/abrasion |
| membrane tension | anchored saddle surface | stress lines from anchors | local thickness/translucency variation |

---

# 9. ROOT GENERATOR REQUIREMENTS FOR FUTURE PR #6+ REVISION

Current provider r4 is blocked for pivot normalization. When morphology progresses beyond blockout, a production root generator should expose parameters conceptually equivalent to:

- `parent_radius_m`
- `child_radius_ratio`
- `load_vector`
- `reaction_growth_vector`
- `cross_section_ellipticity`
- `cross_section_centroid_offset`
- `buttress_height_ratio`
- `mechanical_to_hydraulic_role`
- `graft_state = none | natural_fusion | human_graft`
- `wound_age_state`
- `traffic_contact_mask`
- `fiber_direction`

Exact API/naming belongs to the provider owner; this is a morphology requirement, not a cross-scope implementation.

---

# 10. MATERIAL / LOOKDEV CONSEQUENCES

Final material team should not make a single stochastic bark shader.

At minimum support masks/variants for:
- high-load mature fiber;
- distal transport tissue;
- young growth;
- reaction tissue;
- callus/wound wood;
- active wound;
- repeated-contact surface;
- natural fusion;
- human-graft interface;
- local moisture/deposition.

These do not all need separate material slots; they can be parameterized masks if runtime budget permits.

---

# 11. Art-review questions grounded in biomechanics

For a hero root/buttress/graft:

1. Which mass is supported?
2. Where is the largest bending moment?
3. Does section geometry adapt to that load?
4. Where does hydraulic/transport function remain visible?
5. Is growth symmetric for a reason, or just because the modeling tool made it symmetric?
6. Is a junction natural fusion or human graft?
7. If damaged, what stage of wound response is visible?
8. If trafficked, where is contact wear and compensating growth?
9. Does every tertiary ridge align with stress/growth, or is it noise?
10. Could the shape still make sense with all textures disabled?

A “no” on questions 1, 3, 6 or 10 blocks hero-quality approval.

---

# 12. Reference handling

All sources above are used for **mechanistic research only**.

- Do not copy paper figures, diagrams or microscopy images into shipped art without explicit licensing review.
- Do not reproduce an individual real species 1:1 unless that is deliberately required and provenance is documented.
- Translate mechanical/anatomical principles into original Sylva morphology.
- Scientific uncertainty must stay visible in documentation.
- Sylva canon takes precedence over attempts to retrofit fiction into real biology; scientific references constrain plausibility, not lore.
