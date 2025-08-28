<!---
This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.
You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The Dual-Mode ALU is a configurable arithmetic logic unit that can operate in two distinct modes:

### 8-bit Mode (MODE = 0)
In this mode, the ALU processes single 8-bit operations using the full width of both operands:
- **Operand A**: 8-bit value from `uio[7:0]`
- **Operand B**: 4-bit value from `ui[3:0]` (extended to 8-bit internally)
- **Result**: Single 8-bit output on `uo[7:0]`

### Dual 4-bit Mode (MODE = 1)
In this mode, the ALU simultaneously performs two independent 4-bit operations in parallel:
- **High Operation**: `A[7:4] op B[7:4]` → `Result[7:4]`
- **Low Operation**: `A[3:0] op B[3:0]` → `Result[3:0]`
- **Result**: Two 4-bit results concatenated as 8-bit output

### Supported Operations
The ALU supports 8 different operations controlled by the 3-bit opcode `ui[6:4]`:

| Opcode | Operation | Description |
|--------|-----------|-------------|
| 000    | ADD       | Addition (A + B) |
| 001    | SUB       | Subtraction (A - B) |
| 010    | AND       | Bitwise AND (A & B) |
| 011    | OR        | Bitwise OR (A \| B) |
| 100    | XOR       | Bitwise XOR (A ^ B) |
| 101    | SHL       | Shift Left by 1 (A << 1) |
| 110    | SHR       | Shift Right by 1 (A >> 1) |
| 111    | NOT       | Bitwise NOT (~A) |

### Architecture Benefits
- **Resource Sharing**: Common control logic and operation decoders
- **Parallel Processing**: Double throughput in 4-bit mode
- **Configurable Precision**: Single bit switches between modes
- **Efficient Design**: Modular structure with optimized gate count (~650-800 gates)

## How to test

### Basic Testing Setup

1. **Power up** the design and ensure `rst_n` is high
2. **Set inputs** according to the desired test case
3. **Read output** from `uo[7:0]` after propagation delay

### Pin Configuration

**Input Pins:**
- `ui[7]` - Mode Select (0 = 8-bit, 1 = dual 4-bit)
- `ui[6:4]` - Operation Code (3-bit)
- `ui[3:0]` - Operand B (4-bit)
- `uio[7:0]` - Operand A (8-bit, configured as input)

**Output Pins:**
- `uo[7:0]` - ALU Result (8-bit)

### Test Cases

#### 8-bit Mode Tests (ui[7] = 0)

**Addition Test:**
```
ui = 8'b0_000_0101  // Mode=0, OP=ADD, B=5
uio_in = 8'b00000011  // A=3
Expected uo_out = 8'b00001000  // 3+5=8
```

**Subtraction Test:**
```
ui = 8'b0_001_0011  // Mode=0, OP=SUB, B=3
uio_in = 8'b00001000  // A=8
Expected uo_out = 8'b00000101  // 8-3=5
```

**Bitwise AND Test:**
```
ui = 8'b0_010_1111  // Mode=0, OP=AND, B=15
uio_in = 8'b10101010  // A=170
Expected uo_out = 8'b00001010  // 170&15=10
```

#### Dual 4-bit Mode Tests (ui[7] = 1)

**Parallel Addition:**
```
ui = 8'b1_000_0011  // Mode=1, OP=ADD, B_low=3
uio_in = 8'b01010001  // A_high=5, A_low=1
Expected uo_out = 8'b01110100  // High:5+0=5, Low:1+3=4
```

**Parallel XOR:**
```
ui = 8'b1_100_1010  // Mode=1, OP=XOR, B_low=10
uio_in = 8'b11110000  // A_high=15, A_low=0
Expected uo_out = 8'b00001010  // High:15^0=15, Low:0^10=10
```

### Verification Steps

1. **Test each operation** in both modes
2. **Verify edge cases** (overflow, underflow)
3. **Check mode switching** functionality
4. **Validate parallel operation** independence in dual 4-bit mode
5. **Measure propagation delay** for timing analysis

### Expected Behavior

- **Combinational Logic**: Output changes immediately with input changes
- **No Clock Required**: Pure combinational design
- **Deterministic Results**: Same inputs always produce same outputs
- **Mode Independence**: Operations work identically in both modes for equivalent bit widths

## External hardware

This project is a purely digital design that operates entirely within the ASIC and does not require any external hardware components. All functionality is implemented using internal logic gates and operates directly with the TinyTapeout interface pins.

**No external components needed:**
- No PMODs required
- No LED displays needed  
- No external clocks required
- No analog components
- No external memory

The design can be tested using only:
- Logic analyzer or oscilloscope (optional, for signal observation)
- Digital pattern generator (for automated testing)
- Basic multimeter (for power supply verification)

All testing can be performed through the standard TinyTapeout breakout board interface by setting the appropriate digital input patterns and observing the output responses.
