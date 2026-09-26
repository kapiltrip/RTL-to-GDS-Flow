// Complete example from Day 12.
module counter #(parameter WIDTH = 4) (
    input wire clk, rst_n, enable,
    output reg [WIDTH-1:0] count
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= {WIDTH{1'b0}};
        else if (enable)
            count <= count + {{(WIDTH-1){1'b0}}, 1'b1};
    end
endmodule

module counter_top (
    input wire clk, rst_n, enable,
    output wire [7:0] count
);
    counter #(.WIDTH(8)) u_counter (
        .clk(clk), .rst_n(rst_n), .enable(enable), .count(count)
    );
endmodule
