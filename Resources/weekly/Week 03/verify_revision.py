"""Run the revision's Verilog snippets and independent four-state/timing checks."""
from pathlib import Path
import json,re,shutil,subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
QA=ROOT/'Resources/tools/pdf/qa/weekly/week03-examples'
QA.mkdir(exist_ok=True)
IVERILOG=shutil.which('iverilog')
VVP=shutil.which('vvp')
assert IVERILOG and VVP,'The installed Icarus compiler and runtime are required.'
source=(HERE/'revision.md').read_text(encoding='utf-8')
blocks=re.findall(r'```verilog\n(.*?)```',source,re.S)
assert len(blocks)==4
paths=[]
for index,code in enumerate(blocks,1):
    path=QA/f'snippet-{index}.v';path.write_text(code,encoding='utf-8');paths.append(path)
results={}

def run(name,tops,files,extra=''):
    if extra:
        path=QA/f'{name}.v';path.write_text(extra,encoding='utf-8');files=[*files,path]
    output=QA/f'{name}.vvp'
    command=[IVERILOG,'-g2005','-Wall']
    for top in tops:command+=['-s',top]
    command+=['-o',str(output),*map(str,files)]
    compile_result=subprocess.run(command,capture_output=True,text=True,timeout=20)
    assert compile_result.returncode==0,compile_result.stderr
    simulation=subprocess.run([VVP,str(output)],capture_output=True,text=True,check=True,timeout=20)
    assert 'FAIL' not in simulation.stdout,simulation.stdout
    results[name]={'output':simulation.stdout.strip(),'compiler_messages':compile_result.stderr.strip()}
    return simulation.stdout

checks=r'''`timescale 1ns/1ps
module pipe(input wire clk, input wire [7:0] d, output reg [7:0] q1,q2);
  initial begin q1=0; q2=0; end
PIPELINE
endmodule
module revision_checks;
  integer failures=0, checks=0, i,j,pc=0,nc=0,ep,en;
  integer at=-1,bt=-1,ct=-1,pt=-1,qt=-1,rt=-1;
  reg [7:0] data=0; wire [7:0] out;
  reg pclk=0; reg [7:0] pd=0; wire [7:0] q1,q2;
  reg signed [7:0] signed_value,signed_shift;
  reg edge_signal; reg [3:0] states=4'bzx10;
  reg a=0,b=0,c=0,p=0,q=0,r=0;
  reg delayed_data=0,inside_delay=0,before_delay=0;
  reg [8:0] sum;
  top dut(.data(data),.out(out));
  pipe pipeline(.clk(pclk),.d(pd),.q1(q1),.q2(q2));
  task ck;
    input ok; input [8*100-1:0] label;
    begin checks=checks+1;
      if(ok !== 1'b1) begin failures=failures+1; $display("FAIL %0s",label); end
    end
  endtask
  always @(posedge edge_signal) pc=pc+1;
  always @(negedge edge_signal) nc=nc+1;
  always @(a) if(a===1'b1) at=$time;
  always @(b) if(b===1'b1) bt=$time;
  always @(c) if(c===1'b1) ct=$time;
  always @(p) if(p===1'b1) pt=$time;
  always @(q) if(q===1'b1) qt=$time;
  always @(r) if(r===1'b1) rt=$time;
  initial begin a=#3 1; b=#8 1; c=#5 1; end
  initial begin p<=#3 1; q<=#8 1; r<=#5 1; end
  initial #4 delayed_data=1;
  initial inside_delay<=#8 delayed_data;
  initial #8 before_delay<=delayed_data;
  initial begin
    data=8'h96; #1; ck(out===8'h96,"parameter override and named ports");
    ck(6'hA5===6'b100101,"sized truncation");
    ck(8'bz01===8'bzzzzzz01,"leading z padding");
    ck(8'bx01===8'bxxxxxx01,"leading x padding");
    ck(8'shF6===-8'sd10,"signed literal interpretation");
    sum={1'b0,8'd240}+{1'b0,8'd32};
    ck(sum===9'd272 && sum[7:0]===8'd16,"carry and narrowing");
    signed_value=-10; signed_shift=signed_value>>>1;
    ck(signed_shift===-8'sd5,"signed arithmetic shift");
    ck((4'b0110&4'b1010)===4'b0010,"bitwise AND");
    ck((4'b0110&&4'b1010)===1'b1,"logical AND");
    ck((&4'b1110)===1'b0 && (^4'b1100)===1'b0,"reductions");
    ck((~4'b0110)===4'b1001 && (!4'b0110)===1'b0,"complements");
    ck({3'b101,2'b10}===5'b10110,"concatenation");
    ck({3{2'b01}}===6'b010101,"replication");
    ck((1'bx==1'bx)===1'bx && (1'bx===1'bx)===1'b1,"equality");
    ck((1'bx ? 4'b1100 : 4'b1010)===4'b1xx0,"unknown-select merge");
    ck((1'b0&1'bx)===1'b0 && (1'b1|1'bx)===1'b1,"controlling bits");
    pd=12; #1 pclk=1; #0.001;
    ck(q1===8'd12 && q2===8'd0,"pipeline first edge");
    pclk=0; pd=7; #1 pclk=1; #0.001;
    ck(q1===8'd7 && q2===8'd12,"pipeline second edge");
    pclk=0; pd=31; #1 pclk=1; #0.001;
    ck(q1===8'd31 && q2===8'd7,"pipeline third edge");
    for(i=0;i<4;i=i+1) for(j=0;j<4;j=j+1) begin
      edge_signal=states[i]; #1; pc=0; nc=0;
      edge_signal=states[j]; #1;
      ep=(i==0 && j!=0) || (i>=2 && j==1);
      en=(i==1 && j!=1) || (i>=2 && j==0);
      ck(pc==ep && nc==en,"all sixteen four-state edge pairs");
    end
    ck(at==3 && bt==11 && ct==16,"cumulative blocking delays");
    ck(pt==3 && qt==8 && rt==5,"independent NBA delays");
    ck(inside_delay===1'b0 && before_delay===1'b1,"RHS sampling time");
    if(failures==0) $display("PASS %0d semantic checks",checks);
    $finish;
  end
endmodule
'''.replace('PIPELINE',blocks[2])
text=run('semantics',['revision_checks'],[paths[0]],checks)
assert 'PASS 38 semantic checks' in text,text
text=run('queue',['queue_check'],[paths[3]])
observations=[line for line in text.splitlines() if line.startswith(('active a=','settled a='))]
assert observations==['active a=0','settled a=1'],text
observer=r'''`timescale 1ns/1ps
module clock_observer;
  integer rises=0,falls=0;
  always @(posedge clock_demo.clk) if($realtime>0) rises=rises+1;
  always @(negedge clock_demo.clk) if($realtime>0) falls=falls+1;
  initial begin
    #24.1;
    if(rises!==3 || falls!==3 || clock_demo.clk!==1'b0) $display("FAIL clock trace");
    else $display("PASS clock edges, period and initialization");
  end
endmodule
'''
assert 'PASS clock' in run('clock',['clock_demo','clock_observer'],[paths[1]],observer)
precision=r'''`timescale 1ns/1ps
module precision_check;
  initial begin
    #2.3456;
    if($realtime<2.345999 || $realtime>2.346001) $display("FAIL precision rounding");
    else $display("PASS precision rounds to 2.346 ns");
    $finish;
  end
endmodule
'''
assert 'PASS precision' in run('precision',['precision_check'],[],precision)
c_compiler=shutil.which('gcc') or shutil.which('clang')
if c_compiler:
    code=re.findall(r'```c\n(.*?)```',source,re.S)[0]
    path=QA/'bambu-function.c'
    path.write_text(code+'\nint main(void) { return !(func(9,4,3,4)==5 && func(9,4,2,4)==13 && func(9,4,2,5)==12); }\n',encoding='utf-8')
    executable=QA/'bambu-function.exe'
    subprocess.run([c_compiler,'-std=c11','-Wall','-Wextra',str(path),'-o',str(executable)],capture_output=True,check=True,timeout=20)
    subprocess.run([str(executable)],check=True,timeout=20)
    results['C function']='Compiled and checked all three stated branch results; no Bambu synthesis run.'
else:results['C function']='Compiler unavailable; branch arithmetic and boundaries reviewed; no Bambu synthesis run.'
(QA/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('PASS: 38 Verilog semantic checks, exact event-region output, clock trace and time-precision example.')
print(results['C function'])
