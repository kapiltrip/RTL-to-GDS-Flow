`timescale 1ns/1ps
module tb_delays;
    assignment_delays dut();
    integer errors;
    task check;
        input [5:0] expected;
        begin
            if ({dut.a,dut.b,dut.c,dut.p,dut.q,dut.r} !== expected) begin
                errors = errors + 1;
                $display("FAIL: delayed values at t=%0t", $time);
            end
        end
    endtask
    initial begin
        errors = 0;
        // Sample just after each event time, after scheduled assignments settle.
        #0.001 check(6'b000000);
        #10 check(6'b100100);
        #10 check(6'b100101);
        #10 check(6'b100111);
        #10 check(6'b110111);
        #20 check(6'b111111);
        if (errors == 0) $display("PASS: blocking and nonblocking delay timeline");
        else $display("FAIL: %0d timeline checks failed", errors);
        $finish;
    end
endmodule
