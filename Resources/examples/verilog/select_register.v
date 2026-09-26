// Complete example from Lesson 06.
module select_register (
    input  wire a,
    input  wire b,
    input  wire select,
    input  wire clk,
    output reg  out
);
    wire y;
    assign y = select ? b : a;
    always @(posedge clk)
        out <= y;
endmodule
