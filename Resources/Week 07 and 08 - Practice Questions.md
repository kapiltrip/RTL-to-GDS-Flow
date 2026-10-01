# Week 7 and Week 8 — Practice questions

VLSI Design Flow: RTL to GDS · NPTEL · Prof. Sneh Saurabh

[PDF](documents/Week%2007%20and%2008%20-%20Practice%20Questions.pdf) · [Master index](../README.md)

<a id="index"></a>
## Index

[Week 7 : Assignment 7](#week7)

[1](#week7-q1) · [2](#week7-q2) · [3](#week7-q3) · [4](#week7-q4) · [5](#week7-q5) · [6](#week7-q6) · [7](#week7-q7) · [8](#week7-q8) · [9](#week7-q9) · [10](#week7-q10)

[Week 8 : Assignment 8](#week8)

[1](#week8-q1) · [2](#week8-q2) · [3](#week8-q3) · [4](#week8-q4) · [5](#week8-q5) · [6](#week8-q6) · [7](#week8-q7) · [8](#week8-q8) · [9](#week8-q9) · [10](#week8-q10)

<a id="week7"></a>
## Week 7 : Assignment 7

[NPTEL source](https://onlinecourses.nptel.ac.in/e-learning/course/noc26_ee147?unitId=108&assessmentId=186)

<a id="week7-q1"></a>
### 1.

Consider the following synchronous circuit:

[![Week 7 question 1 original figure](images/Quizzes/Week%2007/A7Q1.png)](#index)

The following attributes are valid for all the flip-flops: setup time=30 ps, hold time=15 ps, and CLK-to-Q delay=40 ps. The delay of each inverter is 50 ps. The delay of each NAND gate is 80 ps. Ignore the wire delay.

Assume that the clock period is 500 ps. What is the **worst slack** for **setup** at the timing end-point F4/D?

- 0 ps
- 50 ps
- 100 ps
- 150 ps
- 200 ps
- 250 ps
- 300 ps
- 350 ps
- 400 ps
- 450 ps
- 500 ps

[Index](#index)

<a id="week7-q2"></a>
### 2.

For the same question above (i.e. Q 1), what is the **worst slack** for **hold** at the timing end-point F4/D?

- 100 ps
- 105 ps
- 110 ps
- 115 ps
- 120 ps
- 125 ps
- 130 ps
- 135 ps
- 140 ps
- 145 ps
- 150 ps
- 155 ps
- 160 ps

[Index](#index)

<a id="week7-q3"></a>
### 3.

Consider the following synchronous circuit:

[![Week 7 question 3 original figure](images/Quizzes/Week%2007/A7Q3.png)](#index)

The following attributes are valid for the flip-flops FF1 and FF2: setup time=40 ps, hold time=30 ps, and CLK-to-Q delay=15 ps. The delay of each inverter is 15 ps. Ignore the wire delay.

Assume that the period of the clock is 500 ps. What is the **hold slack** at the timing end-point FF2/D?

- -10 ps
- -5 ps
- 0 ps
- 5 ps
- 10 ps
- 15 ps
- 20 ps
- 25 ps
- 35 ps

[Index](#index)

<a id="week7-q4"></a>
### 4.

Consider the following synchronous circuit.

[![Week 7 question 4 original figure](images/Quizzes/Week%2007/A7Q4.png)](#index)

The following attributes are valid for all the flip-flops: setup time=30 ps, hold time=30 ps, and CLK-to-Q delay=20 ps. The delay of each inverter and buffer is 45 ps. The delay of NAND gate is 60 ps. Ignore the wire delay.

Assume that the period of the clock is 500 ps. What is the **setup slack** at the timing end-point F3/D?

- 0 ps
- 50 ps
- 100 ps
- 150 ps
- 200 ps
- 250 ps
- 300 ps
- 350 ps
- 400 ps
- 450 ps
- 500 ps

[Index](#index)

<a id="week7-q5"></a>
### 5.

For the same question above (i.e. Q 4), what is the **hold slack** at the timing end-point F3/D?

- 10 ps
- 20 ps
- 30 ps
- 0 ps
- -10 ps
- -20 ps
- -30 ps

[Index](#index)

<a id="week7-q6"></a>
### 6.

Which of the following are typically employed in the delay calculation for a given stage during Static Timing Analysis?

A.Interconnect model

B.Driver model of the driving cell

C.Yield model for the given technology

- only A
- only B
- only C
- only A, B
- only A, C
- only B, C
- All
- None

[Index](#index)

<a id="week7-q7"></a>
### 7.

Which tool will you employ to compute the hold slack of a synchronous circuit?

- Icarus
- OpenSTA
- VCS
- Conformal
- Bambu

[Index](#index)

<a id="week7-q8"></a>
### 8.

The hold requirement constraint does **NOT** depend on which of the following quantities in a typical synchronous circuit?

- Clock Period
- Data Path Delay
- Delay on the clock path of the launch flip-flop
- Delay on the clock path of the capture flip-flop

[Index](#index)

<a id="week7-q9"></a>
### 9.

Consider the following statements about PBA and GBA.

A.The PBA slack can be greater than the GBA slack for some timing paths

B.The GBA slack can be greater than the PBA slack for some timing paths

C.The PBA slack can be equal to the GBA slack for some timing paths

Which of the above statements are correct?

- only A
- only B
- only C
- only A, B
- only A, C
- only B, C
- All
- None

[Index](#index)

<a id="week7-q10"></a>
### 10.

Which of the following combinations are considered when creating scenarios for multi-mode multi-corner (MMMC) analysis?

- PVT corners for libraries, RC corners for parasitics, Mode-specific SDC files for constraints
- Low VT and High VT libraries, Floorplan corners for placement, Mode-specific SDC files for constraints
- PVT corners for libraries, Floorplan corners for placement, Timing Exceptions for Constraints
- PVT corners for libraries, Floorplan corners for placement, Mode-specific SDC files for constraints

[Index](#index)

<a id="week8"></a>
## Week 8 : Assignment 8

[NPTEL source](https://onlinecourses.nptel.ac.in/e-learning/course/noc26_ee147?unitId=113&assessmentId=187)

<a id="week8-q1"></a>
### 1.

Consider the following synchronous circuit:

[![Week 8 question 1 original figure](images/Quizzes/Week%2008/A8Q1.png)](#index)

The following attributes are valid for all the flip-flops: setup time=30 ps, hold time=20 ps, and CLK-to-Q delay=40 ps. The delay of each inverter is 40 ps. The delay of each NAND gate is 80 ps. Ignore the wire delay.

Assume that we have defined the following constraints in the SDC file (all time units are in picoseconds):

[![Week 8 question 1 original figure](images/Quizzes/Week%2008/A8Q1u.png)](#index)

What is the **setup slack** at the timing end-point F1/D?

- 200 ps
- 220 ps
- 240 ps
- 260 ps
- 280 ps
- 300 ps
- 320 ps
- 340 ps
- 360 ps
- 400 ps

[Index](#index)

<a id="week8-q2"></a>
### 2.

For the question above (Q-1), what is the **hold slack** at the timing end-point F1/D?

- 100 ps
- 120 ps
- 130 ps
- 140 ps
- 150ps
- 160 ps
- 170 ps
- 180 ps
- 190 ps
- 200 ps

[Index](#index)

<a id="week8-q3"></a>
### 3.

For the question above (Q-1), what is the **worst slack** for setup at the timing end-point port out?

- 200 ps
- 220 ps
- 240 ps
- 260 ps
- 280 ps
- 300 ps
- 320 ps
- 340 ps
- 360 ps
- 400 ps

[Index](#index)

<a id="week8-q4"></a>
### 4.

For the question above (Q-1), what is the **worst slack** for hold at the timing end-point port out?

- 200 ps
- 220 ps
- 240 ps
- 260 ps
- 280 ps
- 300 ps
- 320 ps
- 340 ps
- 360 ps
- 400 ps

[Index](#index)

<a id="week8-q5"></a>
### 5.

Which of the following is the SDC command that instructs an STA tool to perform a hold check at the output port?

- set_output_delay
- set_hold_check
- set_both_check
- set_clock_latency
- set_clock_transition
- set_false_path
- set_case_analysis

[Index](#index)

<a id="week8-q6"></a>
### 6.

Which of the following pieces of information is typically needed as input by a technology mapping tool?

A.Unmapped netlist

B.Technology library

C.Testbench for RTL simulation

- only A
- only B
- only C
- only A, B
- only A, C
- only B, C
- All
- None

[Index](#index)

<a id="week8-q7"></a>
### 7.

Which of the following optimization techniques is typically **NOT** targeted for improving timing:

- Restructuring
- Retiming
- Resizing
- Power Gating
- Fanout optimization

[Index](#index)

<a id="week8-q8"></a>
### 8.

Which of the following optimization techniques involves changing logic circuit elements across a flip-flop:

- Restructuring
- Retiming
- Resizing
- Power Gating
- Fanout optimization

[Index](#index)

<a id="week8-q9"></a>
### 9.

Which of the following is/are valid SDC commands:

A.create_my_clock

B.generate_clock

C.create_generated_clock

- only A
- only B
- only C
- only A, B
- only B, C
- only A, C
- all A, B, C
- none

[Index](#index)

<a id="week8-q10"></a>
### 10.

Consider the following timing report generated by OpenSTA. The unit of time is ps.

[![Week 8 question 10 original figure](images/Quizzes/Week%2008/A8Q10.png)](#index)

Which of the following statements are correct?

A.The timing report shows the details of a path starting from port a and ending on port out

B.The external delay at the input port is 910 ps.

C.The report shows a hold timing violation with slack of -85 ps.

- only A
- only B
- only C
- only A, B
- only B, C
- only A, C
- all A, B, C
- none

[Index](#index)

---

Questions and figures: NPTEL, VLSI Design Flow: RTL to GDS, Prof. Sneh Saurabh, July–December 2026 (noc26_ee147). Question-only edition; original wording and figure files retained.

[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) · [NPTEL attribution](https://nptel.ac.in/) · [Licence reference](https://archive.nptel.ac.in/)
