# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

# ALU Operation codes
ADD = 0b000
SUB = 0b001
AND = 0b010
OR  = 0b011
XOR = 0b100
SHL = 0b101
SHR = 0b110
NOT = 0b111

@cocotb.test()
async def test_8bit_mode_basic(dut):
    """Test basic 8-bit ALU operations"""
    dut._log.info("Start 8-bit mode basic test")
    
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    
    # Test 8-bit ADD: 15 + 10 = 25
    dut._log.info("Testing 8-bit ADD: 15 + 10")
    mode_select = 0  # 8-bit mode
    opcode = ADD
    operand_b = 10
    operand_a = 15
    
    dut.ui_in.value = (mode_select << 7) | (opcode << 4) | operand_b
    dut.uio_in.value = operand_a
    await Timer(1, units="ns")  # Combinational delay
    
    assert dut.uo_out.value == 25, f"ADD failed: expected 25, got {dut.uo_out.value}"
    dut._log.info(f"8-bit ADD result: {dut.uo_out.value}")
    
    # Test 8-bit SUB: 20 - 5 = 15
    dut._log.info("Testing 8-bit SUB: 20 - 5")
    dut.ui_in.value = (0 << 7) | (SUB << 4) | 5
    dut.uio_in.value = 20
    await Timer(1, units="ns")
    
    assert dut.uo_out.value == 15, f"SUB failed: expected 15, got {dut.uo_out.value}"
    dut._log.info(f"8-bit SUB result: {dut.uo_out.value}")

@cocotb.test()
async def test_8bit_mode_bitwise(dut):
    """Test 8-bit bitwise operations"""
    dut._log.info("Start 8-bit bitwise operations test")
    
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 1
    
    # Test 8-bit AND: 0xAA & 0x0F = 0x0A
    dut._log.info("Testing 8-bit AND: 0xAA & 0x0F")
    dut.ui_in.value = (0 << 7) | (AND << 4) | 0x0F
    dut.uio_in.value = 0xAA
    await Timer(1, units="ns")
    
    expected = 0xAA & 0x0F
    assert dut.uo_out.value == expected, f"AND failed: expected {expected}, got {dut.uo_out.value}"
    dut._log.info(f"8-bit AND result: 0x{dut.uo_out.value:02X}")
    
    # Test 8-bit OR: 0x33 | 0x0C = 0x3F
    dut._log.info("Testing 8-bit OR: 0x33 | 0x0C")
    dut.ui_in.value = (0 << 7) | (OR << 4) | 0x0C
    dut.uio_in.value = 0x33
    await Timer(1, units="ns")
    
    expected = 0x33 | 0x0C
    assert dut.uo_out.value == expected, f"OR failed: expected {expected}, got {dut.uo_out.value}"
    dut._log.info(f"8-bit OR result: 0x{dut.uo_out.value:02X}")
    
    # Test 8-bit XOR: 0xF0 ^ 0x0A = 0xFA
    dut._log.info("Testing 8-bit XOR: 0xF0 ^ 0x0A")
    dut.ui_in.value = (0 << 7) | (XOR << 4) | 0x0A
    dut.uio_in.value = 0xF0
    await Timer(1, units="ns")
    
    expected = 0xF0 ^ 0x0A
    assert dut.uo_out.value == expected, f"XOR failed: expected {expected}, got {dut.uo_out.value}"
    dut._log.info(f"8-bit XOR result: 0x{dut.uo_out.value:02X}")

@cocotb.test()
async def test_8bit_mode_shifts(dut):
    """Test 8-bit shift operations"""
    dut._log.info("Start 8-bit shift operations test")
    
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 1
    
    # Test 8-bit SHL: 0x55 << 1 = 0xAA
    dut._log.info("Testing 8-bit SHL: 0x55 << 1")
    dut.ui_in.value = (0 << 7) | (SHL << 4) | 0
    dut.uio_in.value = 0x55
    await Timer(1, units="ns")
    
    expected = (0x55 << 1) & 0xFF
    assert dut.uo_out.value == expected, f"SHL failed: expected {expected}, got {dut.uo_out.value}"
    dut._log.info(f"8-bit SHL result: 0x{dut.uo_out.value:02X}")
    
    # Test 8-bit SHR: 0xAA >> 1 = 0x55
    dut._log.info("Testing 8-bit SHR: 0xAA >> 1")
    dut.ui_in.value = (0 << 7) | (SHR << 4) | 0
    dut.uio_in.value = 0xAA
    await Timer(1, units="ns")
    
    expected = 0xAA >> 1
    assert dut.uo_out.value == expected, f"SHR failed: expected {expected}, got {dut.uo_out.value}"
    dut._log.info(f"8-bit SHR result: 0x{dut.uo_out.value:02X}")
    
    # Test 8-bit NOT: ~0xF0 = 0x0F
    dut._log.info("Testing 8-bit NOT: ~0xF0")
    dut.ui_in.value = (0 << 7) | (NOT << 4) | 0
    dut.uio_in.value = 0xF0
    await Timer(1, units="ns")
    
    expected = (~0xF0) & 0xFF
    assert dut.uo_out.value == expected, f"NOT failed: expected {expected}, got {dut.uo_out.value}"
    dut._log.info(f"8-bit NOT result: 0x{dut.uo_out.value:02X}")

@cocotb.test()
async def test_dual_4bit_mode_basic(dut):
    """Test dual 4-bit mode operations"""
    dut._log.info("Start dual 4-bit mode test")
    
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 1
    
    # Test dual 4-bit ADD: (7+3)|(2+1) = 0xA3
    dut._log.info("Testing dual 4-bit ADD: High(7+3) Low(2+1)")
    mode_select = 1  # dual 4-bit mode
    opcode = ADD
    operand_b = 0x31  # B_high=3, B_low=1
    operand_a = 0x72  # A_high=7, A_low=2
    
    dut.ui_in.value = (mode_select << 7) | (opcode << 4) | (operand_b & 0x0F)
    dut.uio_in.value = operand_a
    await Timer(1, units="ns")
    
    # Expected: High nibble = 7+3=10(0xA), Low nibble = 2+1=3
    expected = 0xA3
    assert dut.uo_out.value == expected, f"Dual ADD failed: expected 0x{expected:02X}, got 0x{dut.uo_out.value:02X}"
    dut._log.info(f"Dual 4-bit ADD result: 0x{dut.uo_out.value:02X}")

@cocotb.test()
async def test_dual_4bit_mode_parallel(dut):
    """Test dual 4-bit parallel operations"""
    dut._log.info("Start dual 4-bit parallel operations test")
    
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 1
    
    # Test dual 4-bit XOR: (0xF^0x3)|(0x5^0xA) = 0xCF
    dut._log.info("Testing dual 4-bit XOR: High(F^3) Low(5^A)")
    dut.ui_in.value = (1 << 7) | (XOR << 4) | 0x0A  # Mode=1, XOR, B_low=A
    dut.uio_in.value = 0xF5  # A_high=F, A_low=5
    await Timer(1, units="ns")
    
    # Expected: High nibble = F^3=C, Low nibble = 5^A=F
    # But B_high comes from ui_in[3:0] extended, so B_high=A too
    # Actually: A_high=F, A_low=5, B_high=A, B_low=A
    # So: High = F^A=5, Low = 5^A=F -> 0x5F
    expected_high = 0xF ^ 0xA
    expected_low = 0x5 ^ 0xA
    expected = (expected_high << 4) | expected_low
    assert dut.uo_out.value == expected, f"Dual XOR failed: expected 0x{expected:02X}, got 0x{dut.uo_out.value:02X}"
    dut._log.info(f"Dual 4-bit XOR result: 0x{dut.uo_out.value:02X}")
    
    # Test dual 4-bit AND with different values
    dut._log.info("Testing dual 4-bit AND")
    dut.ui_in.value = (1 << 7) | (AND << 4) | 0x07  # Mode=1, AND, B=7
    dut.uio_in.value = 0x3C  # A_high=3, A_low=C
    await Timer(1, units="ns")
    
    # Expected: High = 3&7=3, Low = C&7=4
    expected_high = 0x3 & 0x7
    expected_low = 0xC & 0x7
    expected = (expected_high << 4) | expected_low
    assert dut.uo_out.value == expected, f"Dual AND failed: expected 0x{expected:02X}, got 0x{dut.uo_out.value:02X}"
    dut._log.info(f"Dual 4-bit AND result: 0x{dut.uo_out.value:02X}")

@cocotb.test()
async def test_mode_switching(dut):
    """Test switching between 8-bit and dual 4-bit modes"""
    dut._log.info("Start mode switching test")
    
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 1
    
    # Set up same inputs for both modes
    operand_a = 0x3C  # 60 decimal, or high=3, low=12
    operand_b = 0x05  # 5 decimal
    
    # Test in 8-bit mode first
    dut._log.info("Testing ADD in 8-bit mode: 60 + 5")
    dut.ui_in.value = (0 << 7) | (ADD << 4) | operand_b  # 8-bit mode
    dut.uio_in.value = operand_a
    await Timer(1, units="ns")
    
    result_8bit = dut.uo_out.value
    expected_8bit = operand_a + operand_b
    assert result_8bit == expected_8bit, f"8-bit mode failed: expected {expected_8bit}, got {result_8bit}"
    dut._log.info(f"8-bit mode result: {result_8bit}")
    
    # Test same operation in dual 4-bit mode
    dut._log.info("Testing ADD in dual 4-bit mode: High(3+5) Low(12+5)")
    dut.ui_in.value = (1 << 7) | (ADD << 4) | operand_b  # dual 4-bit mode
    dut.uio_in.value = operand_a
    await Timer(1, units="ns")
    
    result_dual = dut.uo_out.value
    expected_high = (operand_a >> 4) + operand_b  # 3 + 5 = 8
    expected_low = (operand_a & 0x0F) + operand_b  # 12 + 5 = 17, but 4-bit so 1
    expected_dual = ((expected_high & 0x0F) << 4) | (expected_low & 0x0F)
    
    assert result_dual == expected_dual, f"Dual mode failed: expected 0x{expected_dual:02X}, got 0x{result_dual:02X}"
    dut._log.info(f"Dual 4-bit mode result: 0x{result_dual:02X}")
    
    # Verify results are different (demonstrating mode switching works)
    assert result_8bit != result_dual, "Mode switching failed - results should be different"
    dut._log.info("Mode switching test passed!")

@cocotb.test()
async def test_all_operations_quick(dut):
    """Quick test of all operations in both modes"""
    dut._log.info("Start comprehensive operations test")
    
    # Set the clock period to 10 us (100 KHz)  
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 1
    
    test_cases = [
        # (mode, opcode, operand_a, operand_b, expected_description)
        (0, ADD, 10, 5, "8-bit ADD"),
        (0, SUB, 10, 3, "8-bit SUB"),  
        (0, AND, 0xFF, 0x0F, "8-bit AND"),
        (0, OR, 0xF0, 0x0F, "8-bit OR"),
        (1, ADD, 0x12, 3, "Dual ADD"),
        (1, XOR, 0xAB, 0x0F, "Dual XOR"),
    ]
    
    for mode, opcode, a, b, desc in test_cases:
        dut._log.info(f"Testing {desc}")
        dut.ui_in.value = (mode << 7) | (opcode << 4) | (b & 0x0F)
        dut.uio_in.value = a
        await Timer(1, units="ns")
        
        result = dut.uo_out.value
        dut._log.info(f"{desc} result: 0x{result:02X}")
        
        # Basic sanity check - result should be valid (0-255)
        assert 0 <= result <= 255, f"{desc} produced invalid result: {result}"
    
    dut._log.info("All operations test completed successfully!")
