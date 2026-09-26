`timescale 1ns/1ps
module tb_language;
    reg clk, rst_n, enable, sel;
    reg [7:0] a, b, d;
    wire [7:0] y_wire, y_reg, q1, q2, count8;
    wire [3:0] count4;
    wire registered_bit;
    reg edge_signal;
    integer positive_edges, negative_edges, errors, i;
    integer ordinary_match, z_match, x_match;
    reg [3:0] selector;
    reg signed [7:0] signed_value;
    reg signed [7:0] shifted_signed_value;
    reg [7:0] unsigned_value;

    mux_forms mux(sel, a, b, y_wire, y_reg);
    counter default_counter(clk, rst_n, enable, count4);
    counter_top wide_counter(clk, rst_n, enable, count8);
    pipeline2 pipe(clk, rst_n, d, q1, q2);
    select_register selected_bit(a[0], b[0], sel, clk, registered_bit);

    always @(posedge edge_signal) positive_edges = positive_edges + 1;
    always @(negedge edge_signal) negative_edges = negative_edges + 1;

    task check;
        input condition;
        input [8*100-1:0] label;
        begin
            if (condition !== 1'b1) begin
                $display("FAIL: %0s", label);
                errors = errors + 1;
            end
        end
    endtask

    task pulse;
        begin
            #1 clk = 1;
            #1 clk = 0;
        end
    endtask

    initial begin
        errors = 0;
        clk = 0; rst_n = 1; enable = 1; sel = 0;
        a = 8'hA1; b = 8'hB2; d = 8'd25;
        positive_edges = 0; negative_edges = 0;
        edge_signal = 0;
        #1 rst_n = 0;
        #1;
        check(count4 === 0 && count8 === 0 && q1 === 0 && q2 === 0,
              "asynchronous reset clears state before a clock edge");
        rst_n = 1;
        check(y_wire === a && y_reg === a, "known mux select zero");
        sel = 1;
        #1 check(y_wire === b && y_reg === b, "known mux select one");
        pulse;
        check(q1 === 25 && q2 === 0, "pipeline first sample");
        check(registered_bit === b[0], "Lesson 06 registered mux selection");
        d = 8'd42;
        pulse;
        check(q1 === 42 && q2 === 25, "pipeline keeps previous stage value");
        for (i = 2; i < 260; i = i + 1) pulse;
        check(count4 === 4 && count8 === 4, "default and overridden widths wrap");
        enable = 0;
        pulse;
        check(count4 === 4 && count8 === 4, "disabled counters retain state");

        check(6'h88 === 6'b001000, "literal truncation keeps low six bits");
        check(8'bz1 === 8'bzzzzzzz1, "z padding");
        check(8'bx01 === 8'bxxxxxx01, "x padding");
        check(4'b10?1 === 4'b10z1, "question mark aliases z in literal");
        check((1'bx == 1'bx) === 1'bx, "logical equality can be unknown");
        check((1'bx === 1'bx) === 1'b1, "case equality compares unknowns");
        check((1'bx ? 4'b1010 : 4'b1001) === 4'b10xx,
              "unknown conditional merges alternative bits");
        signed_value = -6; unsigned_value = -6;
        check(signed_value === 8'b11111010 && unsigned_value === 250,
              "two's complement has signed and unsigned interpretations");
        shifted_signed_value = signed_value >>> 1;
        check(shifted_signed_value === 8'b11111101, "signed arithmetic shift");
        check(((signed_value >>> 1) === 8'b11111101) === 1'b0,
              "unsigned comparison context can change shift interpretation");
        check((unsigned_value >>> 1) === 8'b01111101, "unsigned zero fill");

        selector = 4'b10x1;
        ordinary_match = 0; z_match = 0; x_match = 0;
        case (selector) 4'b10?1: ordinary_match = 1; endcase
        casez (selector) 4'b10?1: z_match = 1; endcase
        casex (selector) 4'b1001: x_match = 1; endcase
        check(ordinary_match == 0 && z_match == 1 && x_match == 1,
              "case, casez, casex distinguish exact and wildcard matching");
        selector = 4'b10z1; z_match = 0;
        casez (selector) 4'b1001: z_match = 1; endcase
        check(z_match == 1, "casez also ignores z in the selector");

        // Ignore the initial x-to-0 transition; count this deliberate sequence.
        positive_edges = 0; negative_edges = 0;
        edge_signal = 1'bx; #1; // 0 -> x: positive
        edge_signal = 1'bz; #1; // x -> z: neither
        edge_signal = 1'b1; #1; // z -> 1: positive
        edge_signal = 1'bz; #1; // 1 -> z: negative
        edge_signal = 1'bx; #1; // z -> x: neither
        edge_signal = 1'b0; #1; // x -> 0: negative
        edge_signal = 1'b1; #1; // 0 -> 1: positive
        edge_signal = 1'b0; #1; // 1 -> 0: negative
        check(positive_edges == 3 && negative_edges == 3,
              "four-state edge event counts");

        if (errors == 0) $display("PASS: language, parameters, and state checks");
        else $display("FAIL: %0d checks failed", errors);
        $finish;
    end
endmodule
