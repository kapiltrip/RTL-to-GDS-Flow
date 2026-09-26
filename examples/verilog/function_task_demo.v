// Complete example from Day 12.
module function_task_demo;
    function [8:0] add8;
        input [7:0] a, b;
        begin
            add8 = {1'b0, a} + {1'b0, b};
        end
    endfunction

    task show_sum;
        input [7:0] a, b;
        reg [8:0] result;
        begin
            result = add8(a, b);
            $display("%0d + %0d = %0d", a, b, result);
        end
    endtask

    initial begin
        show_sum(8'd200, 8'd100);
        $finish;
    end
endmodule
