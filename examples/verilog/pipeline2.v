// Complete example from Day 12.
module pipeline2 (
    input wire clk, rst_n,
    input wire [7:0] d,
    output reg [7:0] q1, q2
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            q1 <= 8'd0;
            q2 <= 8'd0;
        end else begin
            q1 <= d;
            q2 <= q1;
        end
    end
endmodule
