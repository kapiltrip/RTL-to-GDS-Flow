`timescale 1ns/1ps
module initial_always_demo;
    reg clock, counter;

    initial begin
        clock = 1'b0;
        counter = 1'b0;
    end

    always begin
        #10 clock = ~clock;
    end

    initial begin
        $timeformat(-9, 0, " ns", 0);
        $monitor("t=%0t clock=%b counter=%b", $time, clock, counter);
        #35 $finish;
    end
endmodule
