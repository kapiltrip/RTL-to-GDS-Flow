# Day 09 — Overview of VLSI Design Flow VI — From layout to chip

[Course index](README.md) · Week 2 · [Lecture video](https://www.youtube.com/watch?v=BdIkRSzgV5I) · [Handwritten index](Handwritten%20Index.md)

## Outline

- [Mask data preparation and mask writing](#mask-data-preparation-and-mask-writing)
- [Resolution enhancement](#resolution-enhancement)
- [Wafer fabrication packaging and screening](#wafer-fabrication-packaging-and-screening)

## Mask data preparation and mask writing

![Mask manufacture patterns an absorbing film on a mask blank](images/Day%2009/01-mask.png)

*Video frame: [5:44](https://www.youtube.com/watch?v=BdIkRSzgV5I&t=344s). Mask manufacture patterns an absorbing film on a mask blank*


Layout release is followed by manufacturing-data preparation. **Fracturing** breaks complex layout polygons into shapes supported by the selected mask-writing process. Resolution-enhancement processing can modify the mask geometry so the wafer result more closely matches the intended design. The manufactured mask therefore need not be a literal unchanged copy of every layout outline.

![Kapil’s handwritten notes — Part 1, PDF page 24, lower portion](images/Day%2009/h01-mask.jpg)

*Handwritten source: Part 1, PDF page 24, lower portion.*


Your chromium–resist–substrate sketch shows the lecture's conventional transmissive-mask example. The mask process itself uses patterning:

1. Begin with a suitable transparent substrate carrying an absorbing chromium layer and resist.
2. A writing system exposes the required pattern using an appropriate laser or electron-beam process.
3. Develop the resist. For the positive-tone example, exposed resist is removed.
4. Etch the exposed chromium while remaining resist protects other regions.
5. Strip residual resist, inspect the mask, and repair qualifying defects where the process permits.
6. Add the appropriate protection, such as a pellicle, and qualify the mask for use.

This manufactures the **mask**, which is subsequently used to expose resist on wafers. Mask writing and wafer lithography are related but separate operations. A **pellicle** is a protective membrane positioned so particles are kept away from the mask's pattern plane; requirements vary with lithography technology. The lecture's chromium-on-glass example should not be generalized to all modern mask stacks.

## Resolution enhancement

![Closely spaced features motivate resolution-enhancement methods](images/Day%2009/02-opc.png)

*Video frame: [13:33](https://www.youtube.com/watch?v=BdIkRSzgV5I&t=813s). Closely spaced features motivate resolution-enhancement methods*


**Optical proximity correction (OPC)** intentionally modifies mask patterns to compensate for predictable printing errors. Without compensation, a desired sharp corner can print rounded and a line end can pull back. Added or reshaped features such as serifs or hammerheads change the optical image so the processed wafer approaches the target geometry. Their shape is a means to produce the desired result, not necessarily a shape intended to appear identically on the final wafer.

The lecture discusses 193 nm deep-ultraviolet lithography. This is one lithography technology; not all lithography uses that wavelength. Resolution depends on wavelength, numerical aperture, illumination, process, and computational enhancement. [ASML's lithography explanation](https://www.asml.com/en/technology/lithography-principles) provides the physical context.

![Kapil’s handwritten notes — Part 2, PDF page 1; handwritten page 24](images/Day%2009/h02-opc.jpg)

*Handwritten source: Part 2, PDF page 1; handwritten page 24.*


Your L-shaped drawing captures precompensation: a modified mask is chosen because the printing process distorts it toward the intended result. Your “hammerhead, serif, mouse bite” list is a set of illustrative correction shapes. Modern OPC is model-based and process-dependent, so these shapes are not manual universal recipes.

**Double or multiple patterning** separates features into groups that are patterned in separate steps. In the lecture's layout-coloring illustration, neighboring features too close for one exposure receive different colors. Each group has easier spacing within that exposure, while their combined result forms the dense intended pattern. The colors label processing groups; they are not literal colored material on the wafer.

This decomposition introduces extra processing, masks, overlay requirements, and possible coloring conflicts. OPC changes how a pattern prints; pattern decomposition changes which features are formed together. They solve related resolution problems through different mechanisms and can be used together.

### Read the geometry: width spacing pitch and overlay

**Line width** is the distance across a feature. **Spacing** is the edge-to-edge gap between adjacent features. **Pitch** is the distance between corresponding points on repeating features, commonly their centerlines. For equal-width parallel lines with a uniform gap, $p=w+s$. A 20 nm line followed by a 20 nm gap has 40 nm pitch; width and pitch are different measurements.

Consider four ideal line centers at 0, 40, 80, and 120 nm. An illustrative two-mask decomposition assigns alternating lines:

| Patterning group | Line-center positions | Pitch within that group |
|---|---|---|
| A | 0 and 80 nm | 80 nm |
| B | 40 and 120 nm | 80 nm |
| Combined target | 0, 40, 80, and 120 nm | 40 nm |

Each group has more generous spacing, while the combined target remains dense. These numbers demonstrate decomposition; they are not a claim about a particular foundry process. Not every multiple-patterning method uses two independent exposures arranged this way.

**Overlay error** is misregistration between patterns that must align. If group B shifts right by 3 nm while A stays fixed, the combined centers become 0, 43, 80, and 123 nm. Adjacent center distances alternate between 43 and 37 nm. With unchanged 20 nm widths, the gaps become 23 and 17 nm. Thus a placement error can shrink one gap even though each line has the intended width. This is why the handwritten coloring example must be understood together with alignment requirements.

**Check your understanding:** OPC corrects predictable printing distortion in the pattern; decomposition decides which features belong to each patterning group. Identify which operation is being shown before interpreting a modified corner or a colored line.

## Wafer fabrication packaging and screening

![A package provides electrical, thermal, and mechanical support](images/Day%2009/03-package.png)

*Video frame: [22:57](https://www.youtube.com/watch?v=BdIkRSzgV5I&t=1377s). A package provides electrical, thermal, and mechanical support*


Wafer fabrication repeats many operations, including deposition, oxidation, lithography, etching, implantation, cleaning, and thermal processing. **Front end of line (FEOL)** forms transistor/device structures; **back end of line (BEOL)** forms much of the interconnect above them, with contact-related processing often distinguished as middle of line. The detailed sequence depends on the process.

After fabrication, wafer test identifies acceptable dies, the wafer is diced, and suitable dies proceed to packaging. A **package** provides external electrical connections, mechanical protection, and a thermal path. It also adds parasitic resistance, inductance, and capacitance, so it affects signal and power integrity. A **dual in-line package (DIP)** places leads along two sides; a **ball grid array (BGA)** uses a grid of solder-ball connections. Package choice is an electrical and thermal design decision as well as a mechanical one.

![Kapil’s handwritten notes — Part 2, PDF page 2, upper portion; handwritten page 25](images/Day%2009/h03-package.jpg)

*Handwritten source: Part 2, PDF page 2, upper portion; handwritten page 25.*


Your “heat dissipation” point means that generated heat must leave the die through a designed thermal path. A package may use lids, heat spreaders, or external cooling, depending on the product; not every package includes a separate heatsink. Excess temperature can reduce reliability or trigger failure well before literal silicon melting.

**Final test** checks the packaged part, including problems introduced or revealed by packaging. **Burn-in** is controlled electrical/thermal stress used where required to expose certain early-life weaknesses. It is an engineered screening procedure with specified limits, not an instruction to apply arbitrary high voltage. The bathtub curve is a conceptual failure-rate model: early failures, a comparatively stable useful-life region, then wear-out. Actual product reliability must be established for the product and use conditions.

**Binning** sorts manufactured parts by measured characteristics such as supported speed, leakage, power, or functional capability. Two dies made from the same design can have different measured performance because fabrication varies. A lower speed bin can still be a fully conforming product at its own specification. Binning does not repair a faulty design, and price is not determined by frequency alone.

**Recall checks:** Why can mask geometry differ from desired wafer geometry? How does multiple patterning change the spacing problem? Why is test repeated after packaging?

[Previous: Day 08](Day%2008.md) · [Next: Day 10](Day%2010.md)
