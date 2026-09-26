# Day 01 — Basic Concepts of Integrated Circuit I

[Course index](README.md) · Week 1 · [Lecture video](https://www.youtube.com/watch?v=9QgdNsl9qwk)

This lesson connects the physical construction of a chip to the design files that eventually become manufacturing patterns. Its central idea is that a circuit is designed once, then its geometry is reproduced across many dies and wafers.

## Outline

| Topic, rendered below | What to understand |
|---|---|
| [Integration and scaling](#integration-and-scaling) | Monolithic integration, replication, Moore's observation, and design complexity |
| [Devices and interconnect](#devices-and-interconnect) | CMOS inverter, dielectric, metal layers, contacts, and vias |
| [Why routing uses multiple layers](#why-routing-uses-multiple-layers) | Crossing in a drawing versus an electrical connection |
| [Photolithography](#photolithography) | The complete positive-resist pattern-transfer sequence |
| [Ingot, wafer, die, and chip](#ingot-wafer-die-and-chip) | What is grown, sliced, patterned, tested, and packaged |
| [Design, fabrication, and the PDK](#design-fabrication-and-the-pdk) | How process information connects the designer and the foundry |
| [Points to remember](#points-to-remember) | Common errors and recall questions |

## Integration and scaling

![The lecture's historical perspective on integrated circuits and Moore's prediction](images/Day%2001/01-scaling.png)

*Video frame: [09:15](https://www.youtube.com/watch?v=9QgdNsl9qwk&t=555s). The slide links monolithic integration, photolithography, and increasing component count.*

An **integrated circuit (IC)** contains interconnected electronic devices fabricated together on a common substrate. In the silicon technology discussed here, transistors and other structures are formed in and above a silicon wafer. A **monolithic** IC is built as one integrated piece; it is not assembled by soldering a collection of separately packaged transistors onto a board. Single-crystal silicon is the usual starting material in this example, but “monolithic” describes integration into one piece and should not be treated as a universal definition of the substrate's crystallinity.

A board containing separate components also implements a circuit. Its assembly, however, requires many separate parts and external connections. Integration makes the structures smaller and allows many copies to be fabricated with a common sequence of process steps. The expensive design and mask preparation can be shared across a large production run. This is the physical basis of the lecture's “copying” argument: the layout is reproduced, rather than every transistor being individually assembled by hand.

**Moore's law** is a historical observation and projection about economically useful component integration. The lecture distinguishes the original annual doubling estimate from the later estimate of roughly two years. It is not a physical law, a guarantee that every product doubles its transistor count, or a promise that clock frequency doubles. Technology names such as “65 nm” identify process generations; they should not automatically be read as the exact length of every transistor or wire in a modern process.

Shrinking structures can increase density and can improve energy or speed, but the benefits depend on the process and design. More transistors also mean more states, paths, connections, and constraints to verify. The course's design flow is needed because increasing manufacturing capability creates a growing design-management problem.

### Your handwritten note: integration

![Kapil's integration and Moore's-law notes, Part 1 page 1](images/Day%2001/h01-integration.jpg)

Your comparison between discrete components and an IC captures the key manufacturing change: many devices are formed together and connected by patterned material layers. “Monolithic” means one integrated piece. Photolithography helps reproduce the geometry; it is one operation inside a much longer fabrication sequence. The historical doubling interval is an observation about integration, not a guarantee that all chip properties improve at the same rate.

## Devices and interconnect

![CMOS inverter schematic and a cross-section showing devices, metal layers, dielectric, and vias](images/Day%2001/02-ic-layers.png)

*Video frame: [15:38](https://www.youtube.com/watch?v=9QgdNsl9qwk&t=938s). Read the figure from the silicon substrate upward, then compare it with the inverter schematic on the left.*

The **CMOS inverter** uses a PMOS pull-up device connected toward the positive supply and an NMOS pull-down device connected toward ground. Their gates share the input; their output terminals meet at the output node. In the ideal steady-state switch model:

| Input | PMOS | NMOS | Output |
|---|---|---|---|
| Low | Conducting | Off | Pulled high |
| High | Off | Conducting | Pulled low |

This table describes the logical function. It does not mean the transition takes zero time or draws zero current. The output capacitance shown on the schematic must charge or discharge through a finite drive resistance. During switching, both devices can conduct briefly; leakage also prevents a real inverter from having exactly zero static current.

The cross-section explains how that schematic can exist physically. The lower structures form the devices: substrate and wells, doped source/drain regions, and the gate stack. Above them, **interconnect** carries signals and power between devices. The metal conductors are separated by **dielectric**, an electrically insulating material. A conductor on one layer does not automatically contact a conductor on another layer.

A **via** is a deliberately formed conductive connection between interconnect levels. A **contact** connects a device terminal or suitable lower-level structure into the interconnect system; exact naming depends on the process. The gate dielectric is different from a via: its job is insulation while allowing the gate's electric field to control the channel. Confusing the two would change the transistor into a short circuit.

The drawing is a conceptual cross-section, not a complete process recipe or a universal layer stack. Real dimensions, allowed layers, and connection rules come from the chosen process. [SKY130's process-stack documentation](https://skywater-pdk.readthedocs.io/en/main/rules/assumptions.html) is an example of such process-specific information.

### Your handwritten note: the layer stack

![Kapil's drawing of device and interconnect layers, Part 1 page 1](images/Day%2001/h02-layers.jpg)

Read your cross-section vertically: devices perform switching near the substrate, and metal levels provide connections above them. Dielectric separates conductors. A via deliberately bridges two levels. Read the A/B crossing drawing as a connectivity problem: the two paths may overlap in a top view while occupying different heights, so they need not short together.

## Why routing uses multiple layers

![Lecture diagram of crossing connections on separate metal layers](images/Day%2001/04-multilayer-routing.png)

*Video frame: [19:35](https://www.youtube.com/watch?v=9QgdNsl9qwk&t=1175s).*

The lecture's routing puzzle places two pairs of terminals around a bounded region. With alternating terminals on the boundary, connecting each pair inside a single plane forces a crossing. If both paths are conductors in the same layer, that crossing joins the nets electrically.

Moving one path into a different metal layer solves this particular problem. The dielectric keeps the crossing conductors separate; vias are added only where a net intentionally changes layers. A top view can therefore show two lines crossing even though no electrical connection exists between them. A netlist records intended connectivity, while layout adds geometry and layer identity.

More layers provide routing freedom but do not remove constraints. Wires and vias still consume area and have resistance and capacitance. A route must satisfy both connectivity and the process's geometric rules. This is why physical routing is more demanding than drawing arbitrary lines between logic symbols.

## Photolithography

![The complete lecture diagram for film deposition, photoresist application, exposure, development, etching, and photoresist removal](images/Day%2001/03-photolithography.png)

*Video frame: [27:58](https://www.youtube.com/watch?v=9QgdNsl9qwk&t=1678s). Follow the arrows across the top row and back across the bottom row. Orange is photoresist, blue is the film being patterned, and yellow is the substrate.*

**Photolithography** defines a spatial pattern in a light-sensitive resist using optical exposure and development. A subsequent operation, such as etching, transfers that resist pattern into another material. The lecture groups these operations into one explanatory sequence. Keeping the operations separate makes it clear which material is changing at each step.

A **photomask** carries the pattern used during exposure. In the lecture's simplified transmissive-mask example, transparent regions pass light and opaque regions block it. The **photoresist** is a temporary light-sensitive coating on the wafer. It is neither the final interconnect nor the silicon substrate. [ASML's lithography explanation](https://www.asml.com/en/technology/lithography-principles) describes the projection principle behind this pattern transfer.

### 1. Prepare the film to be patterned

The starting picture has a continuous deposited film on the substrate. This film might be an insulator or another process material. Its eventual function depends on the layer being fabricated. Deposition gives material coverage; it does not yet define the openings in the slide.

### 2. Apply and prepare the resist

A liquid resist is dispensed and spread by spinning the wafer. A suitable bake removes solvent and prepares the coating for exposure. Thickness and uniformity matter: if some regions are much thicker than others, exposure and later pattern transfer may behave differently across the wafer. The resist must also adhere well enough to protect the intended regions during processing.

### 3. Align and expose

The exposure system positions the pattern relative to previously fabricated structures, then exposes selected resist regions. Light changes the resist chemistry and hence its response to the developer. At this stage a chemical difference exists in the resist; the desired openings have not simply been burned through the deposited film.

Alignment matters because a correctly shaped contact opening at the wrong location can miss its intended terminal or touch an unintended conductor. **Overlay** describes the alignment relationship between patterns from different processing steps. **Critical dimension** describes an important patterned feature size, such as a line width or opening width. They are separate requirements: a feature can have the right size and still be misplaced.

### 4. Develop the resist

The lecture shows **positive resist**: the exposed portions become more soluble in the developer and are removed, leaving windows in the resist. The unexposed regions remain as a protective pattern. In **negative resist**, exposure makes the exposed regions less soluble relative to the unexposed regions, reversing which portions remain after development.

The statement “light-exposed resist is removed” therefore needs the positive-resist qualification. It is not true for every resist process. [ASML's manufacturing overview](https://www.asml.com/en/company/stories/2021/semiconductor-manufacturing-process-steps) distinguishes the two resist behaviors and places lithography and etching in the wider manufacturing sequence.

### 5. Etch the exposed film

Etching removes the film in the windows where resist no longer protects it. The patterned resist acts as a temporary mask. **Etch selectivity** describes the relative rates at which different materials are removed. A useful process removes the target material quickly enough while preserving sufficient masking material and controlling attack on the underlying material.

The lecture's statement that the etchant does not react with resist is an idealized explanation. Real resist can erode; what matters is adequate selectivity, thickness, and process control. An isotropic etch can remove material sideways as well as vertically, potentially undercutting the mask. A strongly directional etch helps preserve steep sidewalls. The choice follows the feature and material requirements.

### 6. Strip the remaining resist

Once the film pattern is transferred, the remaining resist is removed. In the final picture, the blue film carries the pattern and the orange temporary coating is gone. Resist removal is not the same operation as developing the exposed resist earlier: development created the mask pattern, while stripping removes the mask after it has served its purpose.

### Trace one opening through the entire sequence

Consider a transparent opening on the lecture's mask. Light reaches the resist underneath it. In a positive-resist process, that exposed resist is removed during development. The deposited film becomes accessible there, so etching removes it. After resist stripping, an opening remains in the film. Under an opaque mask region, the resist was initially retained and protected the film, so the film remains.

The causal chain is:

**Mask transmission → local exposure → resist solubility difference → resist opening → film removal.**

The pattern is reused to fabricate many dies. A complete chip requires many aligned process steps; one exposure does not construct every transistor and interconnect layer at once. Real flows can also use implantation masks, hard masks, multiple patterning, and other operations. Those are extensions of the pattern-and-transfer principle, not evidence that the simple slide is a complete fabrication recipe.

### Your handwritten question: what is a mask?

![Your definition of lithography and boxed mask question, Part 1 page 1](images/Day%2001/h07-mask-question.jpg)

*Handwritten source: Part 1, PDF page 1, lower-left question.*

![Kapil's lithography sequence and mask question, Part 1 page 1](images/Day%2001/h03-lithography.jpg)

A **photomask** is a patterned optical template used by a lithography system to control which regions of a light-sensitive resist receive exposure. In a conventional transmissive mask, patterned absorbing material on a transparent substrate controls light transmission. The mask is distinct from the resist: the mask supplies the optical pattern; resist is the temporary coating on the wafer. A reticle commonly carries the pattern projected onto one exposure field, which the tool repeats across the wafer. Some lithography technologies use reflective masks, so “a glass plate that blocks light” is an introductory example rather than a universal definition.

Your sequence is correctly read as **coat → expose → develop → transfer the pattern → strip**. Exposure changes resist chemistry; development removes selected resist; etching removes exposed underlying material. The mask is not pressed into the silicon like a stamp, and UV light does not directly carve the finished metal line. The optical image and process chemistry together determine the printed feature. [ASML explains this pattern-transfer role](https://www.asml.com/en/technology/lithography-principles).

Suppose you want a narrow conductor to remain after subtractive etching. The resist must protect that conductor during the etch. With positive resist, the protected region must remain unexposed in this simplified example. Changing resist tone changes the required mask polarity. This is why “transparent part becomes a wire” is not a general rule: the answer depends on the layer, resist tone, and subsequent process.

Your later notes on optical proximity correction and multiple patterning extend this topic in [Day 09](Day%2009.md#resolution-enhancement).

## Ingot, wafer, die, and chip

![The lecture distinguishes repeated dies on a wafer from a packaged chip](images/Day%2001/05-wafer-die-chip.png)

*Video frame: [36:46](https://www.youtube.com/watch?v=9QgdNsl9qwk&t=2206s). Each small rectangular region represents a separate die location, not an individual transistor.*

| Term | Meaning in this lecture | What happens next |
|---|---|---|
| Ingot | A grown bulk crystal of silicon | Sliced and processed into wafers |
| Wafer | A thin substrate on which many die sites are fabricated | Patterned through many process steps and tested |
| Die | One individual circuit region cut from a processed wafer | Connected and packaged, depending on the product |
| Packaged chip | A die or dies with a package providing protection and external connections | Final testing and system use |

The lecture introduces the Czochralski growth idea: a seed crystal is pulled from a silicon melt while growth conditions are controlled. This explains why the wafer begins as crystalline material. Slicing alone is not the entire wafer-preparation process; surface finishing and other preparation are also needed before device fabrication.

**Yield** is the fraction of manufactured items that meet the relevant acceptance criteria at a specified stage. If 500 tested dies contain 450 acceptable dies, the illustrative die yield is

$$
Y=\frac{450}{500}=0.90=90\%.
$$

The denominator and test stage must be stated. Wafer-level die yield and final packaged-product yield are not automatically identical. A package protects the die and supplies electrical connections, but it also introduces thermal, mechanical, electrical, and testing considerations. In general usage “chip” can also mean bare die; the lecture uses it primarily for the packaged product.

### Your handwritten question: how can we make good or defect-free dies?

![Kapil's ingot, wafer, die and yield notes, Part 1 page 2](images/Day%2001/h04-wafer-yield.jpg)

Your ingot-to-wafer-to-die sequence describes three scales of the same manufacturing chain. In Czochralski growth, a seed contacts molten silicon and is withdrawn under controlled conditions to grow a single-crystal ingot. Wafers are sliced, finished, and processed; dies are the individual circuit regions. The temperature written in the note is an approximate process value, not a setting to memorize as universally exact.

**Answer:** increase the probability of a good die by controlling contamination, process variation, alignment, deposition, etching, and other fabrication steps, and by designing within the process's validated rules. Cleanrooms reduce particles; inspection and metrology detect process drift; design-for-manufacturability measures avoid fragile patterns. Verification removes design mistakes before fabrication. These measures target different causes of failure.

Testing then identifies dies that meet the specified checks; it does not normally repair a broken transistor or turn a defective die into a good one. Some designs include redundancy or repair mechanisms, especially memories, but that must be designed in. No practical process promises that every die is defect-free. **Yield** measures the fraction passing the chosen acceptance criteria, while test coverage measures how effectively a test targets a stated fault model. [Day 08](Day%2008.md#yield-fault-coverage-and-escapes) explains the difference with your numerical examples.

## Design, fabrication, and the PDK

![Lecture diagram connecting a foundry and design team through a PDK](images/Day%2001/06-pdk.png)

*Video frame: [46:21](https://www.youtube.com/watch?v=9QgdNsl9qwk&t=2781s).*

**Design** chooses a circuit organization and physical implementation that meet the required behavior and constraints. **Fabrication** uses a manufacturing process to realize that implementation in material. Separating the businesses does not make the technical tasks independent: a layout is useful only if the chosen process can manufacture it and the resulting devices behave as assumed.

A **process design kit (PDK)** supplies process-specific information used by design tools and engineers. It can include device models, layer definitions, geometric rules, and verification or extraction support. For example, a designer cannot choose arbitrary metal spacing and assume that the foundry will manufacture it reliably. A process rule defines permitted geometry, while device and parasitic models support predictions about electrical behavior. [The SKY130 file-type reference](https://skywater-pdk.readthedocs.io/en/main/contents/file_types.html) shows concrete examples of model and verification files.

The lecture introduces three business models: a **fabless** company concentrates on design and outsources manufacturing; a **merchant foundry** manufactures for customers; an **integrated device manufacturer (IDM)** combines design and manufacturing activities. Real companies may combine business models. The conceptual distinction matters more here than memorizing a company's current classification.

Following design rules improves manufacturability; it does not by itself prove functional correctness or guarantee a particular yield for every design. A design can be geometrically legal but logically wrong. Likewise, fabrication variability, defects, and electrical conditions affect the final outcome. The physical and functional checks address different failure modes.

### Your handwritten notes: business models and process information

![Kapil's design-versus-fabrication and business-model notes, Part 1 page 2](images/Day%2001/h05-industry.jpg)

Your table separates the design investment from the fabrication investment. Design needs engineers, tools, compute, and verification effort; fabrication needs process equipment, facilities, materials, and sustained process control. The useful lifetime and economics of a fab depend on its products and upgrades. A mature process can remain valuable; a newer node does not automatically make an older fab unusable after a fixed number of years.

![Kapil's PDK information loop, Part 1 page 3](images/Day%2001/h06-pdk.jpg)

The arrows are an information contract. The foundry supplies models and rules; the designer creates a circuit and layout compatible with them; the foundry receives manufacturing data. A **design rule** might specify minimum width, spacing, enclosure, or overlap. A **device model** predicts electrical behavior. A **standard-cell library** provides already designed logic building blocks for a particular technology and library family. These are related resources, but the PDK and the cell library are not interchangeable terms.

## Points to remember

- A metal crossing is an electrical junction only if the physical layers and connecting structures make it one.
- Development patterns resist; etching transfers a pattern into another material; stripping removes the remaining resist.
- The positive-resist rule is “exposed regions are removed during development.” Negative resist reverses the retained regions.
- The mask is reused, but each wafer still undergoes physical processing.
- A wafer contains many dies; each die can contain a very large number of devices.
- The PDK connects design assumptions to a specific manufacturing process.

### Recall checks

1. Why can two wires cross in a top-view drawing without being shorted? Identify the role of both the dielectric and the via.
2. If a region is opaque on the mask in the positive-resist example, which materials remain there after development, etching, and stripping?
3. Why does a design-rule-clean layout still need functional verification?
4. If yield improves while wafer cost and gross die count stay fixed, why does the approximate manufacturing cost per good die fall?

[Handwritten source index](Handwritten%20Index.md) · [Next: Day 02](Day%2002.md)
