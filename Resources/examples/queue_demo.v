`timescale 1ns/1ps
module queue_demo;
  reg a;
  initial begin
    a = 1'b0;
    a <= 1'b1;
    $display("active a=%b", a);
    $strobe("settled a=%b", a);
    #1 $finish;
  end
endmodule
