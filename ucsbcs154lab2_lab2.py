import pyrtl

### DECLARE WIRE VECTORS, INPUT, MEMBLOCK ###
alu_out = pyrtl.WireVector(bitwidth=32, name='alu_out')

op = pyrtl.WireVector(bitwidth=6, name='op')
rs = pyrtl.WireVector(bitwidth=5, name='rs')
rt = pyrtl.WireVector(bitwidth=5, name='rt')
rd = pyrtl.WireVector(bitwidth=5, name='rd')
sh = pyrtl.WireVector(bitwidth=5, name='sh')
func = pyrtl.WireVector(bitwidth=6, name='func')

instr = pyrtl.Input(bitwidth=32, name='instr')
rf = pyrtl.MemBlock(bitwidth=32, addrwidth=5, name='rf')

### DECODE INSTRUCTION AND RETRIEVE RF DATA ###
op <<= instr[26:32]
rs <<= instr[21:26]
rt <<= instr[16:21]
rd <<= instr[11:16]
sh <<= instr[6:11]
func <<= instr[0:6]

data0 = rf[rs]
data1 = rf[rt]

### ADD ALU LOGIC HERE ###
with pyrtl.conditional_assignment:
    with func == 0x20:
        alu_out |= data0 + data1
    with func == 0x22:
        alu_out |= data0 - data1
    with func == 0x24:
        alu_out |= data0 & data1
    with func == 0x25:
        alu_out |= data0 | data1
    with func == 0x26:
        alu_out |= data0 ^ data1
    with func == 0x00:
        # alu_out |= data1 << sh
        alu_out |= pyrtl.corecircuits.shift_left_logical(data1, sh)
    with func == 0x02:
        # alu_out |= data1 >> sh
        alu_out |= pyrtl.corecircuits.shift_right_logical(data1, sh)
    with func == 0x3:
        # alu_out |= data1 >> sh
        alu_out |= pyrtl.corecircuits.shift_right_arithmetic(data1, sh)
    with func == 0x2a:
        alu_out |= pyrtl.corecircuits.signed_lt(data0, data1)

### WRITEBACK ###
rf[rd] <<= alu_out