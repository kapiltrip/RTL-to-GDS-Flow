"""Check the new Verilog traces and independently recompute worked results."""
from pathlib import Path
from itertools import product, combinations
import re, tempfile, subprocess, shutil, json
from fractions import Fraction
import tkinter

ROOT=Path(__file__).resolve().parents[2]/'Daily Notes'
HERE=Path(__file__).resolve().parent
iverilog=shutil.which('iverilog') or 'C:/iverilog/bin/iverilog.exe'
vvp=shutil.which('vvp') or 'C:/iverilog/bin/vvp.exe'
with tempfile.TemporaryDirectory(prefix='rtl-study-check-') as folder:
    folder=Path(folder)
    checks=[(13,'queue_demo',['active a=0','settled a=1']),
            (18,'tb',['PASS: reset, count and wrap'])]
    for lesson,top,expected in checks:
        day=(lesson-1)//6+1
        source=(ROOT/f'Day {day:02d}.md').read_text(encoding='utf-8')
        chapter=source.split(f'## Lesson {lesson:02d}:',1)[1].split('\n## Lesson ',1)[0]
        code=re.search(r'```verilog\n(.*?)```',chapter,re.S).group(1)
        filename='counter_simulation.v' if top=='tb' else f'{top}.v'
        file=HERE/filename;file.write_text(code,encoding='utf-8')
        output=folder/(top+'.vvp')
        subprocess.run([iverilog,'-g2012','-s',top,'-o',str(output),str(file)],check=True,capture_output=True,text=True)
        result=subprocess.run([vvp,str(output)],check=True,capture_output=True,text=True,cwd=folder)
        assert all(s in result.stdout for s in expected),result.stdout
        print(result.stdout.strip())
    a=(ROOT/'Day 03.md').read_text(encoding='utf-8')
    for j,code in enumerate(re.findall(r'```verilog\n(.*?)```',a,re.S)):
        if 'module ' not in code:
            # The casez fragment requires its intentionally explicit wrapper.
            wrapped='module casez_demo(input a,b,c,d, output reg y);\n'+code+'\nendmodule\n'
            file=folder/f'fragment-{j}.v';file.write_text(wrapped)
            subprocess.run([iverilog,'-g2012','-s','casez_demo','-o',str(folder/'fragment.vvp'),str(file)],check=True,capture_output=True)

points=list(product([0,1],repeat=3))
f=lambda a,b,c:(a and b) or (a and b and c) or (b and c)
assert [i for i,x in enumerate(points) if f(*x)]==[3,6,7]
assert all(f(a,b,c)==((a and b) or (b and c)) for a,b,c in points)
implicants=[]
for cube in product([0,1,None],repeat=3):
    covered=[i for i,x in enumerate(points) if all(k is None or k==v for k,v in zip(cube,x))]
    if covered and all(f(*points[i]) for i in covered):implicants.append((cube,set(covered)))
primes=[(c,s) for c,s in implicants if not any(s<t for d,t in implicants)]
assert len(implicants)==5 and len(primes)==2
assert all(any(sum(i in t for d,t in primes)==1 for i in s) for c,s in primes)

# Independently enumerate legal cubes for the restored lecture specification,
# then search all small covers instead of merely checking the printed totals.
on={0,1,5,6,7}
legal=[]
for cube in product([0,1,None],repeat=3):
    covered={i for i,x in enumerate(points) if all(k is None or k==v for k,v in zip(cube,x))}
    if covered and covered<=on:legal.append(covered)
prime_sets=[s for s in legal if not any(s<t for t in legal)]
assert {frozenset(s) for s in prime_sets}=={frozenset(s) for s in [{0,1},{1,5},{5,7},{6,7}]}
minimum=next(n for n in range(1,len(legal)+1)
             if any(set().union(*cover)==on for cover in combinations(legal,n)))
assert minimum==3
prime_covers=[cover for cover in combinations(prime_sets,minimum) if set().union(*cover)==on]
assert len(prime_covers)==2
assert all({0,1} in cover and {6,7} in cover for cover in prime_covers)
assert all(((not y) and z) for x,y,z in [(0,0,1),(1,0,1)])
unsat=lambda x,y,z:(x or y) and ((not x) or y) and (not y)
assert not any(unsat(*assignment) for assignment in points)
g=lambda x,y,z:(x and y) or ((not y) and z) or ((not x) and (not z))
assert all(g(x,y,z)==(((not y) or (not z)) if not x else (y or z)) for x,y,z in points)
for a,b,c,d,e in product([0,1],repeat=5):
    raw=(a and c) or (a and d) or (b and c) or (b and d) or (c and e)
    fact=((a or b) and (c or d)) or (c and e)
    alt=((a or b) and d) or ((a or b or e) and c)
    assert raw==fact==alt
assert ((0 or 1) and (1 or 1) and (0 or 1))
assert 3+10==13 and 20-4==16 and 16-13==3
assert 2+11+2+9+2==26 and 15+9-4==20
assert abs(1/(16e-9)/1e6-62.5)<1e-9
assert abs((1.5+.2)-2-(-.3))<1e-9
assert (20+30+40+60)/4==37.5
assert abs((10+1.5-.7-.3)-(1+.8+5.2)-3.5)<1e-9
assert abs((1+.2+.4)-(1.5+.25+.1)-(-.25))<1e-9
print('PASS: implicant counts, restored chart and minimum covers, cofactors, factoring, '
      'SAT witnesses, UNSAT proof, interpolation and timing arithmetic')

# The second depth pass adds examples whose assumptions are independently
# checked here. Exhaustive Boolean checks establish relations, not just totals.
for a,b,c,d in product([0,1],repeat=4):
    selected = c if a else (d if b else 0)
    assert selected == ((a and c) or ((not a) and b and d))
assert not (0 if 1 else 1) and ((1 and 0) or (1 and 1))
for a,b,z in product([0,1],repeat=3):
    clauses = ((not z) or a) and ((not z) or b) and (z or (not a) or (not b))
    assert clauses == (z == (a and b))

output={'A':0,'B':0,'C':1,'D':1}
transition={'A':('A','C'),'B':('B','D'),'C':('C','A'),'D':('D','C')}
partition=[{'A','B'},{'C','D'}]
sizes=[len(partition)]
while True:
    group={state:n for n,states in enumerate(partition) for state in states}
    signatures={}
    for state in output:
        signature=(output[state],*(group[successor] for successor in transition[state]))
        signatures.setdefault(signature,set()).add(state)
    refined=list(signatures.values())
    if {frozenset(g) for g in refined}=={frozenset(g) for g in partition}:break
    partition=refined
    sizes.append(len(partition))
assert sizes==[2,3,4]
def moore_trace(state, inputs):
    values=[]
    for value in inputs:
        state=transition[state][value]
        values.append(output[state])
    return values
assert moore_trace('A',[1,1])==[1,0]
assert moore_trace('B',[1,1])==[1,1]

reached={(0,1)}
while True:
    expanded=reached|{(1-q,1-r) for q,r in reached}
    if expanded==reached:break
    reached=expanded
assert reached=={(0,1),(1,0)}
assert all((q^r)==1 for q,r in reached)
assert {(q,r) for q,r in product([0,1],repeat=2) if (q^r)!=1}=={(0,0),(1,1)}
successor={0:1,1:2,2:2,3:3}
reached={0};history=[set(reached)]
while True:
    expanded=reached|{successor[s] for s in reached}
    if expanded==reached:break
    reached=expanded;history.append(set(reached))
assert history==[{0},{0,1},{0,1,2}] and 3 not in reached and 2 in reached
for a,b,c in product([0,1],repeat=3):
    original=(a and b) or (b and c) or (a and c)
    replacement=a or b
    assert (original and c)==(replacement and c)
assert not ((1 and 0) or (0 and 0) or (1 and 0)) and (1 or 0)

F=Fraction
assert (F(13_000_000)-F(1_000_000))/(F(400)-F(100))==40_000
runtime=(1-F(9,10))+F(9,10)/100
assert runtime==F(109,1000) and runtime+F(5,100)==F(159,1000)
assert F(6,10)-F(35,100)==F(25,100)
assert -F(2,10)+F(25,100)==F(5,100)
good=F(9,10);detected=F(1,2)
escapes=(1-good)*(1-detected)
assert escapes/(good+escapes)==F(1,19)
assert 20-abs(3)==17 and 20-abs(2)==18
assert 255+255==510 and 2**8-1<510<=2**9-1
assert (255+1)%256==0
assert [edge%16 for edge in range(14,19)]==[14,15,0,1,2]
state=(0,0);pipeline=[]
for datum in [5,7,9]:
    state=(datum,state[0]);pipeline.append(state)
assert pipeline==[(5,0),(7,5),(9,7)]

def interpolate(s,c):
    low=F(20)+(F(c)-1)*F(10,2)
    high=F(40)+(F(c)-1)*F(20,2)
    return low+(F(s)-10)*((high-low)/20)
assert interpolate(15,F(5,2))==F(275,8)
assert interpolate(20,2)==F(75,2)
assert [interpolate(s,c) for s,c in [(10,1),(10,3),(30,1),(30,3)]]==[20,30,40,60]
assert 2*100+16==216 and 100+2*8==116
independent=F(10)+F(315,100)-F(5,10)-(F(33,10)+F(66,10))
common=F(2)*(F(11,10)-F(9,10))
assert independent==F(275,100) and independent+common==F(315,100)
assert F(4)+F(4,10)-F(5,10)-F(2,10)-(F(2,10)+F(3,10)+F(25,10))==F(7,10)
assert (20-1)-(10+7)==2
assert (5+12)-(5+10)==(8+12)-(8+10)==2
for data,select in [(0,7),(8,0),(2,3)]:
    shared=max(data,select)+1+3
    speculative=max(data+3,select)+1
    assert shared>=speculative
    if select>=data+3:assert shared-speculative==3
    if select<=data:assert shared==speculative

interpreter=tkinter.Tcl()
interpreter.eval('set word {[expr {1+2}]}')
assert interpreter.eval('set copy $word')=='[expr {1+2}]'
assert interpreter.eval('expr {1+2}')=='3'
assert interpreter.eval('set result [expr {1+2}]')=='3'
print('PASS: priority case, gate CNF, FSM refinement, cutpoint invariant, reachability, '
      'fanout counterexample, new numerical derivations and staged Tcl substitution')

# Check the additional depth examples against exhaustive Boolean models and
# independent event timelines. These checks do not claim physical signoff.
for a,b,c,d in product((0,1),repeat=4):
    n1=not (a and b);n2=not (c and d)
    assert (not (n1 and n2))==bool((a and b) or (c and d))
assert (not (0 and 0)) or (not (0 and 0))
assert not ((0 and 0) or (0 and 0))

state=0;updates=[]
for n,datum in enumerate([2,3,4]):
    old=state;state+=datum
    updates.append((n,old,datum,3*n,3*(n+1),state))
assert updates==[(0,0,2,0,3,2),(1,2,3,3,6,5),(2,5,4,6,9,9)]
assert 1*2<3<=1*3

latched=0;naive=[];gated=[]
for time,clock,enable in [(-1,0,0),(0,1,0),(2,1,1),(5,0,1),(10,1,1)]:
    if clock==0:latched=enable
    naive.append((time,clock & enable))
    gated.append((time,clock & latched))
def rising_events(trace):
    return [current[0] for previous,current in zip(trace,trace[1:])
            if previous[1]==0 and current[1]==1]
assert rising_events(naive)==[2,10] and rising_events(gated)==[10]
assert 5-2==3 and 5-0==5
assert latched==1

day2=(ROOT/'Day 02.md').read_text(encoding='utf-8')
command_block=re.search(r'```tcl\n(set output \{results/final netlist\.v\}.*?)```',day2,re.S).group(1)
assert interpreter.eval(command_block).strip()=='results/final netlist.v'
assert int(interpreter.eval('llength $command'))==4
assert [interpreter.eval(f'lindex $command {n}') for n in range(4)]==[
    'file','copy','netlists/top.v','results/final netlist.v']

in_mux=F(6,10);out_mux=F(18,10);adder=F(24,10)
arrivals=[]
for data,select in [(0,7),(8,0),(2,3)]:
    arrivals.append((max(data,select)+in_mux+adder,
                     max(data+adder,select)+out_mux))
assert arrivals==[(F(10),F(88,10)),(F(11),F(122,10)),(F(6),F(62,10))]
assert arrivals[0][0]-arrivals[0][1]==adder+in_mux-out_mux==F(12,10)

on={0,1,2,5,6,7}
def cube_points(cube):
    return {4*a+2*b+c for a,b,c in product((0,1),repeat=3)
            if all(wanted is None or wanted==bit for wanted,bit in zip(cube,(a,b,c)))}
cubes={cube:frozenset(cube_points(cube)) for cube in product((None,0,1),repeat=3)}
legal={cube:points for cube,points in cubes.items() if points and points<=on}
primes={cube:points for cube,points in legal.items()
        if not any(points<larger for larger in legal.values())}
expected_cubes=[(0,0,None),(0,None,0),(None,0,1),(None,1,0),(1,None,1),(1,1,None)]
assert set(primes)==set(expected_cubes)
prime_points=[primes[cube] for cube in expected_cubes]
assert prime_points==[frozenset(x) for x in [{0,1},{0,2},{1,5},{2,6},{5,7},{6,7}]]
assert all(sum(point in covered for covered in prime_points)==2 for point in on)
covers=[selection for count in range(1,7) for selection in combinations(range(6),count)
        if set().union(*(prime_points[i] for i in selection))==on]
assert min(map(len,covers))==3
assert {c for c in covers if len(c)==3}=={(0,3,4),(1,2,5)}
minimal=(0,1,4,5)
assert minimal in covers and all(
    set().union(*(prime_points[i] for i in minimal if i!=removed))!=on
    for removed in minimal)

def equality_bdd(order):
    unique={};nodes={}
    def descend(level,assignment):
        if level==4:
            return int(assignment['a']==assignment['b'] and assignment['c']==assignment['d'])
        variable=order[level]
        low=descend(level+1,{**assignment,variable:0})
        high=descend(level+1,{**assignment,variable:1})
        if low==high:return low
        key=(variable,low,high)
        if key not in unique:
            identifier=len(unique)+2;unique[key]=identifier;nodes[identifier]=key
        return unique[key]
    root=descend(0,{})
    for bits in product((0,1),repeat=4):
        values=dict(zip('abcd',bits));cursor=root
        while cursor>1:
            variable,low,high=nodes[cursor];cursor=high if values[variable] else low
        assert cursor==int(bits[0]==bits[1] and bits[2]==bits[3])
    counts={v:sum(node[0]==v for node in nodes.values()) for v in order}
    return len(nodes),counts
assert equality_bdd('abcd')==(6,{'a':1,'b':2,'c':1,'d':2})
assert equality_bdd('acbd')==(9,{'a':1,'c':2,'b':4,'d':2})

witnesses=[(x1,x2,x3) for x1,x2,x3 in product((0,1),repeat=3)
           if (x1 or x2) and ((not x1) or x2) and (x1 or (not x3))]
assert witnesses==[(0,1,0),(1,1,0),(1,1,1)]
assert all(x2==1 for x1,x2,x3 in witnesses)
assert not any(not x2 for x1,x2,x3 in witnesses)

assert [not bool(a) for a in (0,1)]==[True,False]
for other in (0,1):
    nand=[not bool(a and other) for a in (0,1)]
    xor=[bool(a ^ other) for a in (0,1)]
    assert nand==([True,True] if other==0 else [True,False])
    assert xor==([False,True] if other==0 else [True,False])
assert F(80,100)+F(18,100)+F(8,100)==F(106,100)
assert F(60,100)+F(25,100)+F(5,100)==F(90,100)
early=min(F(17,100)+F(6,100),F(24,100)+F(6,100))
late=max(F(110,100)+F(25,100),F(90,100)+F(25,100))
assert early==F(23,100) and late==F(135,100)
assert F(190,100)-late==F(55,100)
assert early-F(30,100)==-F(7,100)
assert late-F(30,100)==F(105,100)

edge_train={'rise':[10*n for n in range(-2,4)],'fall':[10*n+4 for n in range(-2,4)]}
timing=[]
for launching,capturing,launch in [('rise','fall',0),('fall','rise',4)]:
    capture=min(t for t in edge_train[capturing] if t>launch)
    next_launch=min(t for t in edge_train[launching] if t>capture)
    setup_gap=capture-launch;hold_gap=next_launch-capture
    setup=setup_gap-F(20,100)-F(290,100)-F(30,100)
    hold=hold_gap+F(8,100)+F(12,100)-F(10,100)
    timing.append((setup_gap,setup,hold_gap,hold))
assert timing==[(4,F(60,100),6,F(610,100)),(6,F(260,100),4,F(410,100))]
def absolute_hold(launch_latency,capture_latency,uncertainty):
    new_arrival=10+launch_latency+F(8,100)+F(12,100)
    boundary=4+capture_latency+F(10,100)+uncertainty
    return new_arrival-boundary
baseline=absolute_hold(F(2,10),F(4,10),F(1,10))
assert baseline==F(58,10)
assert absolute_hold(F(2,10),F(5,10),F(1,10))==baseline-F(1,10)
assert absolute_hold(F(2,10),F(4,10),F(2,10))==baseline-F(1,10)
assert absolute_hold(F(3,10),F(4,10),F(1,10))==baseline+F(1,10)
assert 4-F(45,10)==-F(5,10) and 6-3==3
print('PASS: recurrence schedule; NAND polarity; gated-clock timeline; Tcl argument '
      'boundaries; asymmetric speculation; all residual-cover primes and optimums; '
      'BDD orders and truth tables; all CNF witnesses; arc polarity; max/min arrival '
      'propagation; mixed-edge setup/hold pairing and pulse-width margins')
