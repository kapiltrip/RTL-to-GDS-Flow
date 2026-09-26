// Complete example from Lesson 12.
`timescale 1ns/1ps
module assignment_delays;
    reg a, b, c, p, q, r;
    initial begin
        a = 0; b = 0; c = 0;
        a = #10 1'b1;
        b = #30 1'b1;
        c = #20 1'b1;
    end
    initial begin
        p = 0; q = 0; r = 0;
        p <= #10 1'b1;
        q <= #30 1'b1;
        r <= #20 1'b1;
    end
    initial begin
        $monitor("t=%0t a=%b b=%b c=%b p=%b q=%b r=%b",
                 $time, a, b, c, p, q, r);
        #61 $finish;
    end
endmodule
