"""Update reader guidance from the completed Weeks 8-12 source/PDF checks."""
import sys
if "--apply-historical-import" not in sys.argv:
    raise SystemExit("Historical import only. Read Resources/tools/sources/README.md before using --apply-historical-import.")

from pathlib import Path
from urllib.parse import quote
import json, re, sys, hashlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
QA=ROOT/'Resources/tools/pdf/qa'
manifest=json.loads((QA/'build-manifest.json').read_text(encoding='utf-8'))
register=json.loads((ROOT/'Resources/sources/study-register.json').read_text(encoding='utf-8'))
pages={p['key']:p for p in register['handwritten_new_pages']}

def source_link(key):
    p=pages[key]
    return f'../Daily%20Notes/Day%20{p["day"]:02d}.md#{p["anchor"]}'

questions=[
('C-03','Why subtract the 20 ps capture-clock offset?',
 'A later external capture clock adds setup time. The equivalent maximum output delay is 400+30−20=410 ps. Hold needs its own minimum-delay equation.'),
('C-06','Can a mapping discard the complement of AB+C?',
 'Preserve Boolean polarity through every NAND/inverter. The toy library comparison measures area/power and the relevant path arcs separately.'),
('C-10','Which input arrives late in the AND-chain example?',
 'B arrives at 70 ps; C/D/A arrive at 20/30/40 ps. The lecture chain gives 220 ps, the handwritten reordered chain 180 ps, and a separate balanced alternative 170 ps.'),
('C-12','May one register move across only one mux input?',
 'Retiming needs consistent state and cycle alignment on every affected mux input, including select. Reset, enables and visible latency can restrict the transformation.'),
('C-13','Does dynamic power require a factor of one-half?',
 'It depends on activity convention: 0→1 events use αCV²f; counting all transitions can introduce one-half under the corresponding balanced-event assumptions.'),
('C-17','Does sleep=1 turn on the drawn PMOS header?',
 'No. A high gate turns that PMOS header off. Supply gating, retention and isolation need coordinated controls; verify the actual switch polarity.'),
('C-19','Why put a latch before the clock-gating AND?',
 'A transparent-low latch allows the enable to settle while the clock is low and holds it stable throughout the high pulse, avoiding extra truncated edges.'),
('D-01','In which order are scan bits loaded?',
 'Each shift uses old Q values. Under SI→FF1→FF2→FF3→SO, loading state 110 requires serial bits 0,1,1; palindrome 101 conceals the reversal.'),
('D-02','Does a 501,000-edge estimate include separate unloading?',
 'That estimate overlaps readout with the next load for 1000 patterns and a 500-cell chain, plus final readout/protocol overhead. Separate load/unload is about 1,001,000 edges.'),
('D-03','Does a failed propagation path prove redundancy?',
 'Try all legal alternatives or prove identical good/faulty output functions. The added G3-output stuck-at-zero example is redundant, but its stuck-at-one counterpart is detectable.'),
('D-04','Is NAND controlling value one because its output can be one?',
 'The controlling input is zero. Detecting the drawn NAND output stuck at one requires full vector 1100 and noncontrolling side inputs along propagation.'),
('N-01','Why backtrack the top network but classify the lower fault as redundant?',
 'The top fault reaches Z with A=X, B=1, C=0, D=0 after its Y-path conflict. For the lower branch fault, all eight input assignments preserve the same Boolean output.'),
('D-07','Are successive LFSR states independent random vectors?',
 'No. The written seed and recurrence deterministically cycle through seven nonzero states. The OR-fault miss probabilities are a separate independent-random teaching model.'),
('D-13','Does every coupled victim show the same glitch?',
 'Coupling, ground capacitance, aggressor edge and victim restoring drive matter. The 0.2 V capacitive-divider example assumes an initially floating victim.'),
('D-16','Which area is the utilization denominator?',
 'State the report convention. In the example, 4500 µm² of cells is 60% of eligible area but 45% of total core area after accounting for macros/blockages.'),
('E-04','Is 30 ps global skew the signed skew of every path?',
 'Global skew is latest minus earliest sink arrival. Each launch/capture pair instead uses signed S=C−L to evaluate setup and hold.'),
('E-06','Does useful skew make the combinational logic faster?',
 'It redistributes time between the 200/300 ps stages. The ideal period changes 300→250 ps; adding 45 ps overhead gives 295 ps, and other paths/hold still require checks.'),
('E-07','Can a lower clock frequency repair this same-edge hold failure?',
 'The same-edge hold inequality contains capture/launch arrivals and minimum data delay, not the next period. The worked skew change turns +20 ps into −30 ps hold slack.'),
('E-08','Does zero global overflow prove detailed routability?',
 'No. A coarse guide does not prove legal pin access, wire/via spacing, enclosure or detailed geometry.'),
('E-14','Can fill and redundant vias be added after final extraction without rechecking?',
 'They change geometry and possibly parasitics/current behavior. Re-extract and repeat the affected analyses on the changed final layout.'),
('E-18','Do DRC and LVS certify the same property?',
 'DRC checks permitted geometry; LVS compares extracted connectivity/devices with the reference. Both can pass independently of timing or the intended algorithm.'),
('E-19','Can a metal-only ECO reprogram an already manufactured chip?',
 'It can reduce which masks change for a manufacturing revision when spare cells are usable. It does not physically rewire existing silicon through software.'),
]
file=ROOT/'Resources/Questions.md'
text=file.read_text(encoding='utf-8').split('\n## October 3 continuation')[0].rstrip()
text+='\n\n## October 3 continuation\n\nCorrections and assumptions are developed beside the complete original source pages. These entries provide direct routes to that reasoning.\n\n| Page | Question | Clarification | Deep explanation |\n|---|---|---|---|\n'
for key, question, answer in questions:
    text+=f'| {key} | {question} | {answer} | [Explanation]({source_link(key)}) |\n'
file.write_text(text,encoding='utf-8')

file=ROOT/'Resources/Glossary.md'
text=file.read_text(encoding='utf-8').split('\n## Final-week terminology')[0].rstrip()
text+='\n\n## Final-week terminology\n\nThese additions accompany the detailed Days 07–09 explanations.\n\n| Term | Expansion | Meaning | Explanation |\n|---|---|---|---|\n'
for term, expansion, meaning, key in [
 ('DVFS','Dynamic Voltage and Frequency Scaling','Changes voltage and frequency together; distinguish power from energy for a fixed task.','C-16'),
 ('LFSR','Linear Feedback Shift Register','Deterministic shift/XOR recurrence; taps, convention and seed set its sequence.','D-07'),
 ('MISR','Multiple-Input Signature Register','Compacts several response bits per step into a finite signature, with possible aliasing.','D-08'),
 ('HPWL','Half-Perimeter Wire Length','Bounding-box estimate used in placement; does not specify a legal routed tree.','D-23'),
 ('EM','Electromigration','Current/stress-related material transport requiring technology-qualified reliability limits.','D-20'),
 ('ESR','Equivalent Series Resistance','A capacitor model includes resistive loss and voltage drop in addition to ideal charge storage.','D-21'),
 ('ESL','Equivalent Series Inductance','A capacitor connection/model has inductance that limits rapid current delivery.','D-21'),
 ('CTS skew','Capture arrival minus launch arrival, S=C−L','Positive pair skew adds setup margin and removes hold margin for the stated same-clock path.','E-07'),
 ('ECO','Engineering Change Order','A controlled connectivity/geometry change followed by renewed affected verification.','E-19')]:
    text+=f'| {term} | {expansion} | {meaning} | [Explanation]({source_link(key)}) |\n'
file.write_text(text,encoding='utf-8')

file=ROOT/'Resources/README.md'
text=file.read_text(encoding='utf-8').replace('all 60 readable source pages','all 128 readable source pages')
text=text.replace('all six daily PDFs','all nine daily PDFs')
text=text.replace('Downloaded lecture decks and scratch files remain in the ignored `.work` directory.',
 'The Week 12 lecture decks are maintained in `sources/lectures/week12`. Earlier download scratch files remain in the ignored `.work` directory; caption-review exports and rendered QA pages remain in `tools/pdf/qa`.')
text=text.replace('all 60 original-page mappings, four readable source-PDF page counts, 32 completed lessons',
 'all 128 original-page mappings, eight readable source-PDF page counts, 54 completed lessons')
text=text.replace('python Resources/tools/pdf/check_collection.py\n',
 'python Resources/tools/pdf/check_collection.py\npython Resources/tools/pdf/check_wrapup_examples.py\n')
file.write_text(text,encoding='utf-8')

file=ROOT/'Resources/Study Guide.md'
text=file.read_text(encoding='utf-8').split('\n## Revising the final weeks')[0].rstrip()
text+='\n\n## Revising the final weeks\n\nUse Days 06–09 in order when rebuilding the reasoning from constraints to tapeout. For a focused Week 12 review, start at [Day 09](../Daily%20Notes/Day%2009.md#day-09-index). Each full source page has its own explanation; lecture frames link to the demonstrated segment.\n\n'
text+='| Study block | Reproduce without looking |\n|---|---|\n'
text+='| Day 06 | Derive input/output delay signs, calculate every mapped path, and compare the original, rewired and Shannon-decomposed timing examples. |\n'
text+='| Day 07 | Account for event energy/activity, explain clock versus power gating, shift a non-palindromic scan vector, and justify a complete ATPG test or redundancy proof. |\n'
text+='| Day 08 | Generate the seven-state LFSR, state aliasing assumptions, calculate wire resistance/coupled voltage and supply drop, and allocate one cross-block timing budget. |\n'
text+='| Day 09 | Calculate HPWL, explain buffered-wire delay, reproduce useful skew and the hold failure, distinguish guides from final geometry, and connect each signoff check with its required input artifacts. |\n\n'
text+='At the end, follow one register transfer through placement, CTS, routing, extraction and STA. Then explain why a final ECO or fill change can require renewed physical, parasitic and timing checks. The connected design story at the end of Lesson 54 ties those dependencies together.\n'
file.write_text(text,encoding='utf-8')
print('Updated correction routes, final-week terminology, resource guide and revision guidance.')

if '--final' in sys.argv:
    # The page list is recorded only after inspecting the final rendered
    # contact sheets and full-page details. Require the matching PDF bytes.
    visual=json.loads((QA/'visual-review-wrapup.json').read_text(encoding='utf-8'))
    for day in range(6,10):
        review=visual['days'][str(day)]
        pdf=ROOT/'PDFs'/manifest[str(day)]['filename']
        assert review['pages_reviewed']==list(range(1,manifest[str(day)]['pages']+1))
        assert review['pdf_sha256']==hashlib.sha256(pdf.read_bytes()).hexdigest()
    navigation=json.loads((QA/'navigation-detail.json').read_text(encoding='utf-8'))
    checks=json.loads((QA/'checks.json').read_text(encoding='utf-8'))
    for day in range(6,10):
        pdf=ROOT/'PDFs'/manifest[str(day)]['filename']
        assert navigation[str(day)]['pdf_sha256']==hashlib.sha256(pdf.read_bytes()).hexdigest()
        assert not checks[str(day)]['geometry_issues']

    file=ROOT/'Resources/Coverage Review.md'
    text=file.read_text(encoding='utf-8').split('\n## October completion review')[0].rstrip()
    text=re.sub(r'Reviewed on \*\*1 October 2026\*\*.*?(?=\n\n## Review by day)',
      'Updated on **4 October 2026**, through Kapil\'s reported completion of **Week 12**. '
      'All **128 readable source pages** have page-to-explanation mappings, and all **54 course items**, '
      'including tutorials, have lesson sections. The October continuation adds 68 source pages and 22 '
      'course items after Constraints I. Nine six-lesson study blocks are complete.',text,flags=re.S)
    text=re.sub(r'^\| \[06\].*$',
      '| [06](../Daily%20Notes/Day%2006.md) | 31–36 | Scan B, pages 9–11; Scan C, pages 1–12 | 15 | '
      'Clock/SDC modeling; external input/output delay signs; mapped-cell polarity and timing; '
      'late-input rewiring, Shannon decomposition, buffering and retiming with state alignment. |\n'
      '| [07](../Daily%20Notes/Day%2007.md) | 37–42 | Scan C, pages 13–24; Scan D, pages 1–4; ATPG notebook | 17 | '
      'Switching/internal/leakage power; DVFS energy; power gating and retention; glitch-free clock enable; '
      'scan bit ordering/cost; activation, propagation, backtracking and redundancy proofs. |\n'
      '| [08](../Daily%20Notes/Day%2008.md) | 43–48 | Scan D, pages 5–21 | 17 | '
      'LFSR recurrence/aliasing; implantation and BEOL; wire RC/crosstalk; interface timing budgets; '
      'eligible-area utilization; macro halos/orientations; PDN, IR, transient droop, decoupling and EM. |\n'
      '| [09](../Daily%20Notes/Day%2009.md) | 49–54 | Scan D, pages 22–24; Scan E, pages 1–19 | 22 | '
      'HPWL/density/legalization; scan reordering/ECO spares; buffered clock wire; latency/skew/meshes; '
      'useful-skew setup and hold; global/detailed routing; fill, extraction, DRC/ERC/LVS and final signoff. |',
      text,flags=re.M)
    text=text.replace('individual 60 page-to-explanation mappings','individual 128 page-to-explanation mappings')
    text=text.replace('All six PDFs now','All nine PDFs now')
    text=text.replace('Each day now contains two further worked explanations',
                      'Days 01–06 also contain two further worked explanations')
    text=re.sub(r'The maintained collection checker now verifies all 60.*?(?= The PDF checker)',
      'The maintained collection checker verifies all 128 original page identities, all eight readable '
      'source-PDF page counts, their explanation links, complete October-page images, all 54 lesson '
      'identities, current progress and lecture-capture hashes.',text,flags=re.S)
    total=sum(m['pages'] for m in manifest.values())
    figures=sum(m['figures'] for m in manifest.values())
    headings=sum(len(m['headings']) for m in manifest.values())
    blocks=sum(m['code_blocks'] for m in manifest.values())
    text=re.sub(r'The six exported PDFs contain.*?(?=\n\n## Source limits)',
      f'The nine exported daily PDFs contain **{total} pages**. All **{figures} figure rectangles**, '
      f'**{total} footer rectangles** and **{headings} heading bookmarks** have verified navigation '
      f'targets. All {blocks} code blocks and retained paragraphs pass exported-content checks. '
      'The four changed PDFs were rendered and visually inspected on every page; geometry checks '
      'report no issues. The earlier five PDFs retain their previous verified content.',text,flags=re.S)
    text=text.replace('The third new upload, `Data/Scan-Empty-Upload.pdf`,',
                      'The earlier September upload, `Data/Scan-Empty-Upload.pdf`,')
    text=text.replace('The readable inventory is Part 1 (24), Part 2 (4), Scan A (21) and Scan B (11), totaling 60.',
      'The readable inventory is Part 1 (24), Part 2 (4), Scans A/B (21/11), '
      'Scans C/D/E (24/24/19) and the digital ATPG notebook (1), totaling 128.')
    text=re.sub(r'The completed boundary remains.*?(?=\n|$)',
      'The completed boundary is **Day 09, Lesson 06 of the day, course Lesson 54**. '
      'The third October scan contains 19 PDF pages, rather than the initial estimate of 11.',text)
    text+='\n\n## October completion review\n\n'
    text+='The four changed PDFs contain **'+str(sum(manifest[str(d)]['pages'] for d in range(6,10)))+' pages**: '
    text+=', '.join(f'Day {d:02d} ({manifest[str(d)]["pages"]})' for d in range(6,10))+'. '
    text+='They preserve every new source page and include **26 actual player frames** captured in Chrome across Lessons 33–54. The 22 caption exports were used as local review material; PDFs contain selected screenshots and original explanations. Week 12 primary slide decks are also preserved.\n\n'
    text+='The final-week explanations derive long-wire repeater delay, distinguish source-to-sink latency from signed pair skew and global skew range, recompute the 300→250 ps useful-skew example and its 295 ps extension, and show a hold slack falling from +20 to −30 ps. They then follow demand/capacity into pin/via legality, connect fill/rerouting to extraction, and distinguish the geometry, connectivity, timing and supply questions at signoff. Lesson 54 follows one register transfer through the complete data chain.\n\n'
    text+='The new teaching-model checker exhaustively compares good/faulty functions in the two ATPG notebook circuits and the reconvergent D-03 circuit, verifies the complete NAND test vector and scan loading order, and enumerates all seven nonzero LFSR states. It independently recomputes timing transformations, scan edge estimates, random-model miss probabilities, DVFS power/energy ratios, wire resistance, coupled voltage, supply drop, decoupling and EM unit conversion. These are checks of stated analytical examples. The review does not claim a newly executed local ASIC flow or foundry-qualified signoff.\n\n'
    changed_pages=sum(manifest[str(d)]['pages'] for d in range(6,10))
    text+=f'The visual pass checks all {changed_pages} pages of the changed reading set, including the contents, complete scan edges, lecture captions, equations, tables, code and references. Sparse-page flags arise mainly when the next complete source image requires a fresh page; those images remain large enough to read. A stray maintenance label identified in the draft was removed before the final page review.\n'
    file.write_text(text,encoding='utf-8')
    print(f'Updated final coverage review: {total} daily pages, {figures} figures, '
          f'{headings} heading bookmarks, {blocks} code blocks; every changed PDF page visually checked.')
