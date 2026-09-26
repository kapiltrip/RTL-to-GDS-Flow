# Run in a practice directory: this writes tcl_demo_output.txt.
set values {0 1 2 3 4 5 6}
set index -1
foreach element $values {
    incr index
    if {$element % 2 == 0} {
        lset values $index [expr {-$element}]
    }
    puts "index=$index values=$values"
}

proc sum_product {x y} {
    set sum [expr {$x + $y}]
    set product [expr {$x * $y}]
    return [list $sum $product]
}
puts [sum_product 10 50]

set fp [open "tcl_demo_output.txt" w+]
puts $fp "test"
close $fp

set fp [open "tcl_demo_output.txt" r]
set file_data [read $fp]
close $fp
puts -nonewline $file_data
