"""Verify the small models added in the 4 October notebook-depth iteration.

This checks actual HDL simulation, exhaustive finite models and dimensional
calculations. It does not run or certify a complete ASIC implementation flow.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
import hashlib
import json
import math
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / 'Resources/tools/pdf/qa'
QA.mkdir(parents=True, exist_ok=True)
results = {}


def hdl_program(day, module):
    source = (ROOT/'Daily Notes'/f'Day {day:02}.md').read_text(encoding='utf-8')
    blocks = re.findall(r'```verilog\n(.*?)```', source, re.S)
    matches = [b for b in blocks if re.search(r'\bmodule\s+'+module+r'\b', b)]
    assert len(matches) == 1, module
    return matches[0]


def executable(name):
    path = shutil.which(name) or str(Path('C:/iverilog/bin')/(name+'.exe'))
    assert Path(path).is_file(), f'Icarus {name} is required on PATH.'
    return path


with tempfile.TemporaryDirectory(prefix='rtl-depth-') as directory:
    folder = Path(directory)
    compiler, runner = executable('iverilog'), executable('vvp')

    def simulate(top, source, expected):
        code = folder/(top+'.v')
        output = folder/(top+'.vvp')
        code.write_text(source, encoding='utf-8')
        subprocess.run([compiler, '-g2005', '-s', top, '-o', str(output), str(code)],
                       capture_output=True, text=True, check=True)
        run = subprocess.run([runner, str(output)], cwd=folder,
                             capture_output=True, text=True, check=True)
        assert expected in run.stdout, run.stdout
        return run.stdout.strip()

    unknown_tb = r'''
module tb_unknown;
  reg sel;
  reg [3:0] a,b,want;
  wire [3:0] yc,yi;
  integer k,i,j,bitno,count;
  unknown_select dut(sel,a,b,yc,yi);
  initial begin
    count=0;
    for(k=0;k<4;k=k+1) begin
      case(k) 0:sel=0; 1:sel=1; 2:sel=1'bx; 3:sel=1'bz; endcase
      for(i=0;i<16;i=i+1) for(j=0;j<16;j=j+1) begin
        a=i; b=j; #1;
        if(k==0) want=b;
        else if(k==1) want=a;
        else for(bitno=0;bitno<4;bitno=bitno+1)
          want[bitno]=(a[bitno]===b[bitno]) ? a[bitno] : 1'bx;
        if(yc!==want) begin $display("FAIL: conditional"); $finish(1); end
        if(yi!==((k==1)?a:b)) begin $display("FAIL: if"); $finish(1); end
        count=count+1;
      end
    end
    $display("PASS: unknown mux 1024 cases (%0d)",count); $finish;
  end
endmodule
'''
    results['four_state_mux'] = simulate('tb_unknown', hdl_program(2,'unknown_select')+unknown_tb,
                                         'PASS: unknown mux 1024 cases (1024)')
    results['delayed_rhs_sampling'] = simulate('delayed_samples', hdl_program(2,'delayed_samples'),
                                               'inside=0 before=1')
    signed_tb = r'''
module tb_signed;
  reg signed [7:0] x,division,floorq,corrected;
  integer i,count;
  initial begin
    count=0;
    for(i=-128;i<128;i=i+1) begin
      x=i;
      division=x/8'sd4;
      floorq=x>>>2;
      corrected=floorq;
      if(x[7] && (|x[1:0])) corrected=floorq+8'sd1;
      if(division!==corrected) begin $display("FAIL: signed %0d",x); $finish(1); end
      if(i==-7 && (division!=-1 || floorq!=-2)) begin
        $display("FAIL: counterexample"); $finish(1);
      end
      count=count+1;
    end
    $display("PASS: signed division 256 cases (%0d)",count); $finish;
  end
endmodule
'''
    results['signed_division_hdl'] = simulate('tb_signed', signed_tb,
                                              'PASS: signed division 256 cases (256)')
    for x in range(-128,128):
        floor = x//4
        fixed = floor + int(x<0 and (x & 3)!=0)
        assert fixed == math.trunc(x/4)

# Independent required-behavior mask, including the changed-specification failure.
care_mismatches = []
changed_spec_mismatches = []
for a,b,c in product((0,1), repeat=3):
    original = (not a) and b
    proposal = bool(b)
    dont_care = a and b
    if not dont_care and original != proposal: care_mismatches.append((a,b,c))
    new_dont_care = a and b and c  # 110 now requires the original zero.
    if not new_dont_care and original != proposal: changed_spec_mismatches.append((a,b,c))
assert care_mismatches == [] and changed_spec_mismatches == [(1,1,0)]
results['cube_care_mask'] = {'assignments':8,'changed_spec_counterexample':'110'}

# Construct an ROBDD by Shannon recursion, unique nodes and redundant-test removal.
def equality_bdd(bits, interleaved):
    order = ([v for i in range(bits) for v in [('A',i),('B',i)]] if interleaved
             else [('A',i) for i in range(bits)]+[('B',i) for i in range(bits)])
    unique = {}
    def visit(level, assignment):
        if level == len(order):
            return int(all(assignment['A',i]==assignment['B',i] for i in range(bits)))
        var = order[level]
        children=[]
        for value in (0,1):
            assignment[var]=value
            children.append(visit(level+1,assignment))
        del assignment[var]
        low,high=children
        if low==high: return low
        key=(var,low,high)
        if key not in unique: unique[key]=len(unique)+2
        return unique[key]
    root=visit(0,{})
    assert root>1
    return len(unique)
counts={n:[equality_bdd(n,True),equality_bdd(n,False)] for n in (2,3,4)}
assert counts=={2:[6,9],3:[9,21],4:[12,45]},counts
results['bdd_orders_nonterminal_nodes']=counts

def successor(q): return 1 if q==0 else (3 if q==2 else 0)
reachable={0}
while True:
    expanded=reachable|{successor(q) for q in reachable}
    if expanded==reachable:break
    reachable=expanded
assert reachable=={0,1}
assert all(q!=3 for q in reachable)
assert [q for q in range(8) if q!=3 and successor(q)==3]==[2]
assert all(successor(q)<2 for q in range(2))
results['reachability_and_induction']={'reachable':sorted(reachable),'unreachable_step_counterexample':2}

def signature(stream):
    s0=s1=0
    for bit in stream: s0,s1=s1,s0^s1^bit
    return s0,s1
streams=list(product((0,1),repeat=3))
zero=[s for s in streams if signature(s)==(0,0)]
assert zero==[(0,0,0),(1,1,1)]
assert signature((0,0,1))==(0,1)
results['signature_aliasing']={'zero_signature_streams':['000','111'],
                              'conditional_nonzero_alias_probability':str(Fraction(1,7))}

# Check the deterministic-pattern gap independently of the random-trial estimate.
state = (0,0,0,0,1)
period = []
while state not in period:
    period.append(state)
    state = state[1:] + (state[0] ^ state[2],)
all_vectors = set(product((0,1), repeat=5))
assert state == (0,0,0,0,1)
assert set(period) == all_vectors - {(0,0,0,0,0)} and len(period) == 31
detecting = [v for v in all_vectors if int(any(v)) != 1]
assert detecting == [(0,0,0,0,0)]
assert not any(v in detecting for v in period)
assert int(any((0,0,0,0,0))) == 0
results['lfsr_missing_or_test'] = {'period':31, 'detecting_vector':'00000',
                                   'detections_in_period':0, 'independent_trial_probability':'1/32'}

def load(chain, bits):
    state=dict.fromkeys(chain,0)
    for bit in bits:
        old=state.copy()
        state[chain[0]]=bit
        for i in range(1,len(chain)):state[chain[i]]=old[chain[i-1]]
    return state
def unload(chain, values):
    state=values.copy();bits=[]
    for _ in chain:
        bits.append(state[chain[-1]])
        old=state.copy();state[chain[0]]=0
        for i in range(1,len(chain)):state[chain[i]]=old[chain[i-1]]
    return bits
desired={'A':1,'B':1,'C':0}
for chain,serial in [('ABC',[0,1,1]),('ACB',[1,0,1])]:
    assert load(chain,serial)==desired
    assert unload(chain,desired)==serial
for patterns in (1,2,7,1000):
    # Explicit operation schedule, including the last unload.
    n=500
    shifts=n + (patterns-1)*n + n
    assert shifts+patterns==(patterns+1)*n+patterns
assert 1000*(2*500+1)==1001000
assert (1000+1)*500+1000==501500
results['scan_protocol']={'orders':{'ABC':'011','ACB':'101'},'exact_overlapped_edges':501500}

# Dimensional calculations use SI units and recompute the values in the notes.
def close(a,b): assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-16),(a,b)
finished=[6000/(500*y)+5 for y in (.8,.5)]
assert finished==[20,29]
assert [9000000/(35-c) for c in finished]==[600000,1500000]
close(1000*(15e-15-5e-15),10e-12)
close(5e-15/(20e-15+5e-15),.2)
close(10e-3*1e-9/(50e-12),.2)
close(.1*10e-3,.001)
close(100e-12*(10e-3/20e-12),.05)
close(100*(20e-15+30e-15)+200*30e-15,11e-12)
assert [(w1+w2)/2+40 for w1,w2 in [(40,40),(40,70),(70,70)]]==[80,95,110]
assert (10-2,6-1)==(8,5) and (6-1,2)==(5,2)
assert (100+5,200+2)==(105,202)
assert (30+(-20))==10 and 13-10==3
for maximum,minimum,want in [(.95,.10,(-.03,.05)),(.60,.03,(.32,-.02))]:
    close(1-.08-maximum,want[0]);close(minimum-.05,want[1])
arrivals=[0,50,100]
skews=[arrivals[1]-arrivals[0],arrivals[2]-arrivals[1],arrivals[0]-arrivals[2]]
assert skews==[50,50,-100] and sum(skews)==0
repairs=[(-30+lo,70-hi) for lo,hi in [(20,35),(35,55),(45,80)]]
assert repairs==[(-10,35),(5,15),(15,-10)]
antenna = [2*(length+.4)*.35/.1 for length in (100,30)]
close(antenna[0],702.8);close(antenna[1],212.8)
assert antenna[0] > 400 > antenna[1]
window_area = 200*200
close((8000+20000)/(2*window_area),.35)
assert 8000/window_area < .3 < 20000/window_area
assert .3*window_area-8000 == 4000
results['final_sanity_physical_models'] = {'antenna_ratios':antenna,
    'density_global_average':.35, 'window_A_legal_fill_area_um2':4000}
results['numeric_and_geometric_models']='yield/cost, signed requirements, scenario matrix, RC, decap, pin transforms, via pitch and ECO budgets'

hashes={str(d):hashlib.sha256((ROOT/'Daily Notes'/f'Day {d:02}.md').read_bytes()).hexdigest()
        for d in range(1,10)}
(QA/'depth-example-checks.json').write_text(json.dumps({'results':results,'source_sha256':hashes},
                                                    indent=2)+'\n',encoding='utf-8')
print('PASS: actual HDL (1024 four-state mux cases, delayed sampling, 256 signed inputs); '
      'care masks, constructed BDDs, reachability/induction, signature collisions, '
      'scan permutations, the missing LFSR/OR test, antenna/density and dimensional calculations.')
