/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */
`default_nettype none

module tt_um_dual_mode_alu (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Input/Output assignments
    wire mode_select = ui_in[7];        // 0 = 8-bit mode, 1 = dual 4-bit mode
    wire [2:0] opcode = ui_in[6:4];     // ALU operation select
    wire [7:0] operand_a = uio_in;      // First operand (8-bit or two 4-bit values)
    wire [7:0] operand_b = ui_in[3:0] ? {ui_in[3:0], ui_in[3:0]} : {4'b0, ui_in[3:0]}; // Second operand
    
    // Internal signals
    wire [7:0] alu_result_8bit;
    wire [7:0] alu_result_dual_4bit;
    wire [7:0] final_result;
    
    // ALU Operations (3-bit opcode)
    localparam ADD  = 3'b000;
    localparam SUB  = 3'b001;
    localparam AND  = 3'b010;
    localparam OR   = 3'b011;
    localparam XOR  = 3'b100;
    localparam SHL  = 3'b101;  // Shift left
    localparam SHR  = 3'b110;  // Shift right
    localparam NOT  = 3'b111;  // Bitwise NOT
    
    // 8-bit ALU implementation
    alu_8bit alu8 (
        .a(operand_a),
        .b(operand_b),
        .opcode(opcode),
        .result(alu_result_8bit)
    );
    
    // Dual 4-bit ALU implementation
    dual_alu_4bit dual_alu4 (
        .a_high(operand_a[7:4]),
        .a_low(operand_a[3:0]),
        .b_high(operand_b[7:4]),
        .b_low(operand_b[3:0]),
        .opcode(opcode),
        .result(alu_result_dual_4bit)
    );
    
    // Mode selection multiplexer
    assign final_result = mode_select ? alu_result_dual_4bit : alu_result_8bit;
    
    // Output assignments
    assign uo_out = final_result;
    assign uio_out = {mode_select, opcode, 4'b0000}; // Status output
    assign uio_oe = 8'hFF; // All uio pins as outputs for status
    
    // List all unused inputs to prevent warnings
    wire _unused = &{ena, clk, rst_n, 1'b0};
    
endmodule

// 8-bit ALU module
module alu_8bit (
    input [7:0] a,
    input [7:0] b,
    input [2:0] opcode,
    output reg [7:0] result
);
    
    always @(*) begin
        case (opcode)
            3'b000: result = a + b;           // ADD
            3'b001: result = a - b;           // SUB
            3'b010: result = a & b;           // AND
            3'b011: result = a | b;           // OR
            3'b100: result = a ^ b;           // XOR
            3'b101: result = a << 1;          // SHL
            3'b110: result = a >> 1;          // SHR
            3'b111: result = ~a;              // NOT
            default: result = 8'b0;
        endcase
    end
    
endmodule

// Dual 4-bit ALU module
module dual_alu_4bit (
    input [3:0] a_high,
    input [3:0] a_low,
    input [3:0] b_high,
    input [3:0] b_low,
    input [2:0] opcode,
    output [7:0] result
);
    
    wire [3:0] result_high, result_low;
    
    // High 4-bit ALU
    alu_4bit alu_h (
        .a(a_high),
        .b(b_high),
        .opcode(opcode),
        .result(result_high)
    );
    
    // Low 4-bit ALU
    alu_4bit alu_l (
        .a(a_low),
        .b(b_low),
        .opcode(opcode),
        .result(result_low)
    );
    
    assign result = {result_high, result_low};
    
endmodule

// 4-bit ALU module
module alu_4bit (
    input [3:0] a,
    input [3:0] b,
    input [2:0] opcode,
    output reg [3:0] result
);
    
    always @(*) begin
        case (opcode)
            3'b000: result = a + b;           // ADD
            3'b001: result = a - b;           // SUB
            3'b010: result = a & b;           // AND
            3'b011: result = a | b;           // OR
            3'b100: result = a ^ b;           // XOR
            3'b101: result = a << 1;          // SHL
            3'b110: result = a >> 1;          // SHR
            3'b111: result = ~a;              // NOT
            default: result = 4'b0;
        endcase
    end
    
endmodule
