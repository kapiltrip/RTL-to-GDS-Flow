# Synopsys RTL to GDS Tool Map

| Step | Process | Tool |
|---|---|---|
| 1 | RTL coding and testbench | HDL editor |
| 2 | RTL lint and clock or reset crossing checks* | VC SpyGlass |
| 3 | Simulation and waveform debug | VCS + Verdi |
| 4 | Logic synthesis | Design Compiler or Fusion Compiler |
| 5 | Scan insertion* | TestMAX DFT |
| 6 | Formal equivalence | Formality |
| 7 | Floorplan and power planning | IC Compiler II or Fusion Compiler |
| 8 | Placement and optimization | IC Compiler II or Fusion Compiler |
| 9 | Clock tree synthesis | IC Compiler II or Fusion Compiler |
| 10 | Global and detailed routing | IC Compiler II or Fusion Compiler |
| 11 | Layout finishing and metal fill | IC Compiler II or Fusion Compiler + IC Validator |
| 12 | Parasitic extraction | StarRC |
| 13 | Static timing analysis and closure | PrimeTime |
| 14 | DRC, LVS, antenna and density checks | IC Validator |
| 15 | Power analysis* | PrimePower or licensed PrimeTime PX |
| 16 | IR drop and electromigration* | RedHawk-SC |
| 17 | Test pattern generation* | TestMAX ATPG |
| 18 | Final GDSII export | IC Compiler II or Fusion Compiler |

**Choose one implementation route:** Design Compiler + IC Compiler II, or Fusion Compiler.

**\* Scope dependent:** Include the checks required by your design and teacher. Lint is recommended; clock and reset crossing checks depend on the design. The full plan covers licenses, libraries and signoff requirements.

[Full project plan](../PDFs/Synopsys%20RTL%20to%20GDS%20Project%20Plan.pdf)
