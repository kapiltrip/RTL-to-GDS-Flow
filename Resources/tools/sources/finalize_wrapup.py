"""Maintain source identity, video annotations and reading progress for Weeks 8-12."""
import sys
if "--apply-historical-import" not in sys.argv:
    raise SystemExit("Historical import only. Read Resources/tools/sources/README.md before using --apply-historical-import.")

from pathlib import Path
from urllib.parse import quote, unquote
import json, re, hashlib

ROOT=Path(__file__).resolve().parents[3]
SOURCES=ROOT/'Resources/sources'
def slug(s):
    return re.sub(r'\s','-',re.sub(r'[^\w\s-]','',s.lower().strip()))
records=json.loads((SOURCES/'wrapup-captures.json').read_text(encoding='utf-8'))
videos=json.loads((SOURCES/'wrapup-lessons.json').read_text(encoding='utf-8'))
annotations={
33:('Translate the external receiver into an output requirement','The frame compares the physical receiver with its virtual analysis counterpart. The 400 ps wire plus 30 ps setup, less the 20 ps later capture clock, gives 410 ps of maximum output delay. The receiving flop is absent from the block netlist, so the SDC transfers its requirement to the output boundary. C-03 derives the signs and treats hold separately.'),
34:('Count every mapped cell and every relevant input arc','The displayed toy mapping uses two NAND1 and two INV1 cells. Their area totals 4+1+4+1=10, and the displayed power measure totals 20+5+20+5=50. A/B cross delays 8+8+4=20, while C crosses 4+8+4=16. These are the slide\'s arbitrary teaching measures; input arrival and actual load must also enter a real path comparison. The inversions preserve the required complement of AB+C.'),
35:('Late-input rewiring changes 220 ps into 180 ps','In the left chain, late B=70 ps crosses three 50 ps gates: the successive arrivals are 120,170,220 ps. In the right chain, early C=20 and D=30 finish by 80 ps, adding A=40 gives 130 ps, and late B crosses only the final gate to give 180 ps. C-10 matches the restructured handwritten circuit and adds a separately evaluated balanced alternative.'),
36:('Recompute the actual tutorial timing report','The native report shows input delay 5 ps, inverter increment 80 ps and arrival 85 ps. Its separate required-time calculation starts from 1000 ps and subtracts output delay 5 ps, giving 995 ps. Slack is therefore 995−85=910 ps. The table below develops the tutorial\'s slew/load experiments; none of those SDC changes is a physical buffer insertion.'),
37:('Charge the wire and every receiving pin','The fanout drawing separates wire and pin capacitances from the driving cell\'s internals. The charging current supplies a total load, not just one receiving gate. The frame\'s energy per complete 0→1→0 cycle is CV². C-13 derives that energy and explains why the activity convention determines whether a one-half appears in the average-power formula.'),
38:('Keep the switch, retention and isolation supplies distinct','The diagram places a high-VT sleep switch on the gated supply and keeps retention state on an always-on supply. Isolation clamps an output while the domain cannot drive a valid value. C-17–C-19 explain switch polarity, sequencing and why clock gating addresses a different power component.'),
39:('A physical short becomes a testable logical model','The upper wire drawing shorts B to ground; the lower logic drawing represents that behavior as B stuck at zero. A=B=1 distinguishes good and faulty AND outputs. This modeling step makes pattern generation tractable, while its coverage remains conditional on how well the selected model represents the defect.'),
40:('SE selects the value captured at the next clock edge','The scan mux chooses D in functional/capture mode and SI in shift mode. Q also feeds serial scan-out in this example. Preserving the storage role does not remove mux timing overhead. D-01 follows the old and new register values explicitly so scan loading and response bit order can be reconstructed.'),
41:('Read the internal-energy table before multiplying by activity','The displayed toy table has different rise and fall event energies. At the shown first-row/first-column point, 1 and 2 fJ average to 1.5 fJ only under equal weighting of the two event types. Average power also needs their event rates. The tutorial\'s electrical/load conditions and its activity assumptions are separate inputs.'),
42:('Activation alone does not make a complete ATPG vector','The highlighted stuck-at-one branch must have good value zero. The NAND producing it therefore needs A=B=1. Passing the difference through the final NAND requires its other input to be one, which the lower OR-plus-inverter path supplies with C=D=0. D-04 completes the vector and compares the final good/faulty outputs.'),
43:('Pseudorandom sequences are repeatable, not independent randomness','The LFSR diagram feeds selected state bits back through XOR logic. Its seed, taps, bit order and update convention determine the entire sequence. D-07 enumerates the seven-state handwritten example; D-08 explains why compressing responses into a signature can alias even when the generator is repeatable.'),
44:('A patterned mask selects where dopants enter','The cross-sections show donor and acceptor implantation through exposed regions, with photoresist protecting others. The beam acceleration/filtering and subsequent annealing serve different purposes: place the desired ions, then activate dopants and repair process damage. D-09 relates this device formation to FEOL and distinguishes it from BEOL wiring.'),
45:('Glitch amplitude depends on the electrical environment','The quiet victim is coupled to the switching aggressor through Cc and to a reference through its ground capacitance. Faster aggressor edges and greater coupling tend to increase disturbance; greater victim capacitance or restoring drive can reduce the voltage excursion. D-13 derives a capacitive-divider approximation and states where it stops being sufficient.'),
46:('The installation tutorial provisions dependencies in WSL','This actual tutorial frame shows dependency packages being fetched in its Ubuntu/WSL environment. It is evidence of the demonstrated setup stage, not a new install on this computer. Matching a tool revision and its supported dependencies is necessary before checking a sample design; the current official setup documentation is linked below.'),
47:('Budget one complete cross-block transfer','The frame follows FF1 through B1, inter-block logic/wire and B3 to FF2. Block-level SDC must describe the time already spent before an input and needed after an output. D-15 allocates an explicit 2 ns path budget; assigning every block the full period would count available time more than once.'),
48:('A halo reserves pin-access space at macro corners','The left macro corner is crowded with a standard cell; the right reserves a halo. The halo is a placement restriction, not automatically a routing ban on every layer. Rotating a macro can change which pins face a channel, but its allowed orientations and power connections must remain legal.'),
49:('Measure the box, then remember what it omits','The two grid drawings enclose the same pin set and count adjacent sides of the box. The lecture obtains 11 unit intervals. An interior pin does not expand the box, even though the final routed tree must still connect it. D-23 supplies explicit coordinates and distinguishes the estimate from a legal multi-pin route.'),
50:('A generated power grid still needs electrical analysis','The tutorial GUI shows power-grid geometry on the GCD floorplan. Its visible warnings include a checkpoint-write issue and an IR view without populated data. A drawn grid is a topology to analyze, while a usable checkpoint/report requires successful generation and the correct analysis inputs.'),
51:('Identify the clock boundary before measuring skew','The diagram labels the generator, declared source and consuming register clock pins. Follow the clock buffers separately from the orange combinational data logic. E-02–E-07 distinguish source-to-sink latency, signed pair skew and global skew range, then connect them to setup and hold.'),
52:('A graph edge represents a limited physical resource','The frame connects three-dimensional layer graphs through via edges and compares USE(e) with CAP(e). Power/clock reservations and obstructions reduce what remains available to signal nets. E-10 distinguishes overflow from congestion and E-12 explains why detailed pin/via rules can still fail after a feasible coarse plan.'),
53:('LVS compares two independently formed circuit descriptions','Merged layout and an extraction deck produce the layout netlist; the design database and library models produce the source netlist. The comparison reports mismatches that must be repaired in the design. E-18 explains why this connectivity check is separate from geometry and timing closure.'),
54:('The script records routing evidence and checkpoints','The tutorial editor shows detailed-routing options, a DRC report path, antenna checks and written database/DEF files, followed by extraction. Each output belongs to a particular design revision. The tutorial explanation below connects those files to the later routed GUI and the required parasitic/timing checks.'),
}
for record in records:
    if record['path'].endswith('/01-lecture-frame.jpg'):
        lesson=record['lesson']; day=(lesson-1)//6+1
        title, explanation=annotations[lesson]
        record['caption']=title
        file=ROOT/'Daily Notes'/f'Day {day:02d}.md'
        text=file.read_text(encoding='utf-8')
        marker=f'<!-- wrapup-frame-{lesson} -->'
        if marker not in text:
            pattern=rf'(^## Lesson {lesson}:.*?\n\n.*?\n\n)'
            mm=re.search(pattern,text,re.M|re.S); assert mm,lesson
            seconds=record['time_seconds']; stamp=f'{seconds//60}:{seconds%60:02d}'
            figure=(f'{marker}\n\n[![{title}](../{quote(record["path"],safe="/")})](#day-{day:02d}-index)\n\n'
                    f'*Lecture: [{stamp} — {title}]({record["url"]}).*\n\n{explanation}\n\n')
            text=text[:mm.end()]+figure+text[mm.end():]
            file.write_text(text,encoding='utf-8')
    assert hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest()==record['sha256']
(SOURCES/'wrapup-captures.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
existing=json.loads((SOURCES/'lecture-captures.json').read_text(encoding='utf-8'))
paths={r['path'] for r in records}
existing=[r for r in existing if r['path'] not in paths]
(SOURCES/'lecture-captures.json').write_text(json.dumps(existing+records,indent=2),encoding='utf-8')

newpages=[]
for day in range(6,10):
    text=(ROOT/'Daily Notes'/f'Day {day:02d}.md').read_text(encoding='utf-8')
    lesson=None
    for line in text.splitlines():
        match=re.match(r'^## Lesson (\d+):',line)
        if match: lesson=int(match[1])
        match=re.match(r'^### ([CDEN]-\d\d): (.+)',line)
        if match:
            key,title=match.groups(); group=key[0]; number=int(key[-2:])
            folder={'C':'scan-c','D':'scan-d','E':'scan-e','N':'notebook-atpg'}[group]
            newpages.append({'key':key,'lesson':lesson,'day':day,'anchor':slug(line[4:]),
                             'path':f'Resources/sources/handwritten/{folder}/h{number:02d}.jpg',
                             'title':title})
assert len(newpages)==68 and len({p['key'] for p in newpages})==68
register_path=SOURCES/'study-register.json'
register=json.loads(register_path.read_text(encoding='utf-8'))
register.update({'reported_progress':'Week 12 complete, as reported by Kapil','as_of':'2026-10-03',
                 'completed_sequence':54,'current_day':9,'current_day_lesson':6,
                 'october_upload_pages':68,'readable_handwritten_pages':128})
register['handwritten_new_pages']=[p for p in register['handwritten_new_pages'] if p['key'][0] not in 'CDEN']+newpages
register_path.write_text(json.dumps(register,indent=2),encoding='utf-8')
index=ROOT/'Resources/Handwritten Index.md'
text=index.read_text(encoding='utf-8').split('\n## October continuation')[0].rstrip()
text+='\n\n## October continuation\n\nThe 3 October uploads contain **24 + 24 + 19 scan pages**, plus **one digital ATPG notebook page**. All 68 are reproduced and explained. PDF source positions remain separate from paper numbers and generated PDF pages.\n\n'
text+='| Source page | Topic | Explanation |\n|---|---|---|\n'
for page in sorted(newpages,key=lambda p:(p['key'][0],p['key'])):
    text+=f'| [{page["key"]}]({page["path"][10:]}) | {page["title"]} | [Day {page["day"]:02d}, Lesson {page["lesson"]}](../Daily%20Notes/Day%20{page["day"]:02d}.md#{page["anchor"]}) |\n'
index.write_text(text,encoding='utf-8')

sourcefile=ROOT/'Resources/Sources.md'
text=sourcefile.read_text(encoding='utf-8').split('\n## Weeks 8–12 continuation')[0].rstrip()
text+='\n\n## Weeks 8–12 continuation\n\nReviewed in Chrome on 3 October 2026 using the official NPTEL outline, lecture segments, captions and actual player screenshots. The 54-item course sequence includes tutorials. Study-day numbers use six lessons; they do not assert laboratory completion.\n\n'
text+='| Course lesson | Week | Primary video | Saved player frames |\n|---|---:|---|---|\n'
for video in videos:
    lesson=video['lesson']; transcript=ROOT/'Resources/tools/pdf/qa/transcripts'/f'lesson-{lesson}.txt'
    assert transcript.is_file(),lesson
    frames=[]
    for record in records:
        if record['lesson']!=lesson: continue
        seconds=record['time_seconds']; stamp=f'{seconds//60}:{seconds%60:02d}'
        frames.append(f'[{stamp}]({quote(record["path"][10:],safe="/")})')
    text+=f'| {lesson} | {video["week"]} | [{video["title"]}](https://www.youtube.com/watch?v={video["id"]}) | '+', '.join(frames)+' |\n'
text+='\nWeek 12 primary slide decks are preserved beside the notes: [CTS](sources/lectures/week12/lecture-40.pdf), [Routing](sources/lectures/week12/lecture-41.pdf), [Signoff](sources/lectures/week12/lecture-42.pdf), and [Tutorial 12](sources/lectures/week12/tutorial-12.pdf). They came from the course-linked [Week 12 material folder](https://drive.google.com/drive/folders/12GNzun_dE9kfmT2qc_Kg9sP5MdG2z_Ll). Course lesson 51 corresponds to printed lecture 40; tutorials explain the numbering difference.\n\n'
refs={
'OpenSTA command reference':'https://opensta.readthedocs.io/en/latest/Commands/',
'OpenROAD setup and flow overview':'https://openroad.readthedocs.io/en/latest/main/README.html',
'OpenROAD Flow Scripts tutorial':'https://openroad-flow-scripts.readthedocs.io/en/latest/tutorials/FlowTutorial.html',
'OpenROAD placement':'https://openroad.readthedocs.io/en/latest/main/src/gpl/README.html',
'OpenROAD power-network generation':'https://openroad.readthedocs.io/en/latest/main/src/pdn/README.html',
'OpenROAD clock-tree synthesis':'https://openroad.readthedocs.io/en/latest/main/src/cts/README.html',
'OpenROAD timing repair':'https://openroad.readthedocs.io/en/latest/main/src/rsz/README.html',
'OpenROAD global routing':'https://openroad.readthedocs.io/en/latest/main/src/grt/README.html',
'OpenROAD detailed routing':'https://openroad.readthedocs.io/en/latest/main/src/drt/README.html',
'OpenRCX parasitic extraction':'https://openroad.readthedocs.io/en/latest/main/src/rcx/README.html'}
text+='Current tool clarification references: '+', '.join(f'[{label}]({url})' for label,url in refs.items())+'. Historical tutorial helper procedures and flags are distinguished from current documented commands.\n'
sourcefile.write_text(text,encoding='utf-8')

top=ROOT/'README.md'; text=top.read_text(encoding='utf-8')
text=re.sub(r'\*\*Current position:.*?(?=\n\n)', '**Current position: Week 12 complete — Day 09, Lesson 06 of the day (course Lesson 54).** Updated from Kapil\'s reported progress on 3 October 2026. Tutorials count in the sequence; the study notes review demonstrations without claiming new laboratory runs.', text,count=1,flags=re.S)
text=re.sub(r'The equal allocation is.*?(?=\n\n)', 'The allocation is **six lessons per study day**: `day = floor((lesson−1)/6)+1`. All 54 course lessons now occupy nine completed study blocks. Equal lesson counts do not imply equal video durations or study effort.',text,count=1,flags=re.S)
rows=[]
for video in videos:
    lesson=video['lesson']; day=(lesson-1)//6+1
    daytext=(ROOT/'Daily Notes'/f'Day {day:02d}.md').read_text(encoding='utf-8')
    title=re.search(rf'^## Lesson {lesson}: (.+)$',daytext,re.M).group(1)
    rows.append(f'| {day:02d} | {video["week"]} | [{lesson:02d} — {title}](Daily%20Notes/Day%20{day:02d}.md#{slug(f"Lesson {lesson}: {title}")}) |')
text=re.sub(r'^\| \d\d \| \d+ \| \[(?:3[3-9]|4\d|5[0-4])[^\n]*\n','',text,flags=re.M)
pattern=r'(\| 06 \| 8 \| \[32[^\n]*\n)'
text=re.sub(pattern,lambda m:m.group(1)+'\n'.join(rows)+'\n',text,count=1)
text=text.replace('Day 01.md to Day 06.md','Day 01.md to Day 09.md').replace('Six daily PDFs','Nine daily PDFs')
text=re.sub(r'All 28 earlier handwritten pages.*?(?=\n\n)', 'All **128 readable source pages** are indexed: 28 earlier pages, 32 pages from Scans A/B, and 68 October additions (Scans C/D/E contain 24/24/19 pages; the ATPG notebook adds one). The earlier zero-byte upload remains preserved separately and contributes no readable pages. Original source-PDF positions, handwritten numbers and generated PDF page numbers remain distinct.',text,count=1,flags=re.S)
top.write_text(text,encoding='utf-8')

data=ROOT/'Resources/Data/README.md'
text=data.read_text(encoding='utf-8').split('\n## October uploads')[0].rstrip()+'\n\n## October uploads\n\n'
for record in json.loads((SOURCES/'october-source-register.json').read_text(encoding='utf-8')):
    text+=f'- [{Path(record["path"]).name}]({quote(Path(record["path"]).name)}) — {record["pages"]} pages; original upload: {record["name"]}.\n'
data.write_text(text,encoding='utf-8')
print('Updated 68 new page mappings, 22 lecture annotations, 26 capture records and Week 12 progress.')
