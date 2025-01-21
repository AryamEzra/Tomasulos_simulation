class Instruction:
    def __init__(self, op, dest, src1, src2):
        self.op = op
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.issue = None
        self.execute_start = None
        self.execute_end = None
        self.write_result = None
        self.status = "waiting"