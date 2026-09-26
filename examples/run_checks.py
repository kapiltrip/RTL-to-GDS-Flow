"""Check the study examples using Icarus Verilog and Python's bundled Tcl."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import tkinter

HERE = Path(__file__).resolve().parent

def executable(name):
    found = shutil.which(name)
    fallback = Path('C:/iverilog/bin') / (name + '.exe')
    if found:
        return found
    if fallback.is_file():
        return str(fallback)
    raise SystemExit(f'{name} is required. Install Icarus Verilog and add its bin directory to PATH.')

def run(command):
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    if result.stderr.strip():
        print(result.stderr.strip())
    return result.stdout

iverilog, vvp = executable('iverilog'), executable('vvp')
files = [str(p) for p in sorted((HERE / 'verilog').glob('*.v'))]
with tempfile.TemporaryDirectory(prefix='rtl-study-') as directory:
    folder = Path(directory)
    for top, expected in [
        ('tb_language', 'PASS: language, parameters, and state checks'),
        ('tb_delays', 'PASS: blocking and nonblocking delay timeline'),
        ('function_task_demo', '200 + 100 = 300'),
    ]:
        output = folder / (top + '.vvp')
        # The examples use traditional Verilog. Explicit language mode avoids
        # accidentally depending on SystemVerilog extensions.
        run([iverilog, '-g2005', '-s', top, '-o', str(output), *files])
        log = run([vvp, str(output)])
        if 'FAIL:' in log or expected not in log:
            raise AssertionError(log)
        print(expected)

    interpreter = tkinter.Tcl()
    previous_directory = Path.cwd()
    try:
        os.chdir(folder)  # The file-I/O example writes only in this temporary folder.
        interpreter.call('source', str(HERE / 'tcl_basics.tcl'))
        assert interpreter.eval('set values') == '0 1 -2 3 -4 5 -6'
        assert interpreter.eval('sum_product 10 50') == '60 500'
        assert interpreter.eval('set file_data') == 'test\n'
        assert (folder / 'tcl_demo_output.txt').read_text() == 'test\n'
        assert interpreter.eval('set literal {[expr {1+2}]}') == '[expr {1+2}]'
    finally:
        os.chdir(previous_directory)
    print('PASS: Tcl list updates, procedure results, literal grouping, and file I/O')
