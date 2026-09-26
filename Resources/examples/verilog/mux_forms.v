// Complete example from Lesson 11.
module mux_forms (
    input  wire       sel,
    input  wire [7:0] a, b,
    output wire [7:0] y_wire,
    output reg  [7:0] y_reg
);
    assign y_wire = sel ? b : a;
    always @* begin
        if (sel) y_reg = b;
        else     y_reg = a;
    end
endmodule
