`timescale 1ns/1ps
module counter(input clk, input rst_n, output reg [3:0] q);
  always @(posedge clk or negedge rst_n)
    if (!rst_n) q <= 4'd0;
    else q <= q + 4'd1;
endmodule

module tb;
  reg clk = 0;
  reg rst_n = 1;
  wire [3:0] q;
  integer expected;
  counter dut(clk, rst_n, q);
  always #5 clk = ~clk;
  initial begin
    $dumpfile("counter.vcd");
    $dumpvars(0, tb);
    expected = 0;
    #1 rst_n = 0;
    #1;
    if (q !== 4'd0) $fatal(1, "reset failed");
    @(negedge clk) rst_n = 1;
    repeat (18) begin
      @(posedge clk);
      #1;
      expected = (expected + 1) % 16;
      if (q !== expected[3:0]) $fatal(1, "count mismatch");
    end
    $display("PASS: reset, count and wrap");
    $finish;
  end
endmodule
