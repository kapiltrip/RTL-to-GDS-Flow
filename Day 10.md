# Day 10 — Introduction to Tcl

[Course index](README.md) · Week 2 · [Lecture video](https://www.youtube.com/watch?v=1fPNZstiL4o) · [Handwritten index](Handwritten%20Index.md)

## Outline

- [Commands variables and substitution](#commands-variables-and-substitution)
- [Control flow and procedures](#control-flow-and-procedures)
- [File channels and external commands](#file-channels-and-external-commands)

## Commands variables and substitution

![Iterate over a list and negate its even elements](images/Day%2010/01-list.png)

*Video frame: [3:11](https://www.youtube.com/watch?v=1fPNZstiL4o&t=191s). Iterate over a list and negate its even elements*


**Tcl** means **Tool Command Language**. The tutorial, presented by Jasmine Kaur, introduces a scripting language widely embedded in EDA tools. Plain Tcl supplies language commands; an EDA application adds commands that manipulate its design database. A command such as `get_cells` is not guaranteed to exist in standalone `tclsh` merely because an EDA tool accepts it.

A Tcl command consists of a command name and words used as arguments. `set index -1` assigns the value `-1` to a variable named `index`. `$index` substitutes its value. Square brackets perform command substitution: `[expr {-$element}]` executes `expr` and substitutes its result. Braces group a word and suppress ordinary substitution at that parsing stage; the command receiving that word may later interpret it as an expression or script. Quotes group words while allowing substitutions.

![Kapil’s handwritten notes — Part 2, PDF page 2, Tcl snippet](images/Day%2010/h01-tcl.jpg)

*Handwritten source: Part 2, PDF page 2, Tcl snippet.*


Your “brackets first” note refers to command substitution in a word where substitution is enabled. It is not a rule that every bracket inside every braced string executes immediately. For example, `puts {[expr {1+2}]}` prints the bracketed text literally; `puts [expr {1+2}]` prints `3`. Bracing expressions is a useful default because the expression evaluator handles their variable substitution and evaluation predictably. [Tcl's `expr` manual](https://www.tcl-lang.org/man/tcl8.6/TclCmd/expr.htm) explains expression evaluation.

This complete version of the lecture's list example uses the same operations:

```tcl
set values {0 1 2 3 4 5 6}
set index -1
foreach element $values {
    incr index
    if {$element % 2 == 0} {
        lset values $index [expr {-$element}]
    }
    puts "index=$index values=$values"
}
```

`foreach` receives the list value at loop entry and assigns each successive element to `element`. `lset` changes the named variable `values` at a zero-based index. `expr` performs arithmetic; `%` gives the integer remainder. The first negation leaves zero unchanged. The final list is `0 1 -2 3 -4 5 -6`. Modifying `values` does not rewrite the iteration list already supplied to this `foreach` invocation.

## Control flow and procedures

`if` selects a branch. `for` has initialization, condition, next-step, and body arguments. `while` repeats while its expression is true. `break` exits the enclosing loop; `continue` skips the remaining body of the current iteration and proceeds with the loop's next iteration. Their Tcl syntax still follows command-and-argument parsing, so braces and spaces have real meaning.

**A procedure** defines a reusable Tcl command with parameters and a body. The following returns both results as a proper Tcl list:

```tcl
proc sum_product {x y} {
    set sum [expr {$x + $y}]
    set product [expr {$x * $y}]
    return [list $sum $product]
}
puts [sum_product 10 50]
```

The output is `60 500`. `return` ends this procedure invocation and provides its result; subsequent statements in that invocation do not run. `puts` prints a value, while returning a value makes it available to the caller. A procedure that prints results is therefore different from one that returns them for another calculation. The lecture demonstrates both printing and early return; this version makes the returned data explicit.

## File channels and external commands

![The file-I/O example prints the text read back from its file](images/Day%2010/02-files.png)

*Video frame: [7:13](https://www.youtube.com/watch?v=1fPNZstiL4o&t=433s). The file-I/O example prints the text read back from its file*


An **open channel** is a handle for I/O. `open` returns a channel identifier; storing it in `fp` lets later commands use `$fp`. Closing a channel releases it and flushes the appropriate buffered output. The tutorial's `w+` mode permits reading and writing and truncates an existing file. Use that mode only for a file whose replacement is intended.

This example should be run in a disposable practice directory because it writes its named demonstration file:

```tcl
set fp [open "tcl_demo_output.txt" w+]
puts $fp "test"
close $fp

set fp [open "tcl_demo_output.txt" r]
set file_data [read $fp]
close $fp
puts -nonewline $file_data
```

The final terminal output is `test` followed by the newline stored in the file. `read` obtains content from the channel's current position. For line-by-line reading, `while {[gets $fp line] >= 0} { ... }` is a robust pattern; `eof` reports channel state after attempted reading, so careless end-of-file loops can mishandle the final read. In production scripts, arrange cleanup even when an intermediate command fails.

`exec` invokes an external program, for example `puts [exec ls]` on a system with `ls`. It does not turn Tcl into a Unix shell: shell syntax and built-ins are not automatically interpreted as they would be by Bash. Tcl already has a native `pwd` command and file commands, which can avoid platform-specific external tools. Save scripts conventionally with `.tcl` and run `tclsh script.tcl`, or use the relevant EDA tool's script mechanism. The extension is a convention, not a magical property that changes the language.

**Practice:** change the list operation to square odd values. Trace the original value of `element`, the current `index`, and the updated list separately. Then modify `sum_product` so the caller selects either result using `lindex`.

The repository contains [complete runnable Tcl examples](examples/tcl_basics.tcl).

[Previous: Day 09](Day%2009.md) · [Next: Day 11](Day%2011.md)
