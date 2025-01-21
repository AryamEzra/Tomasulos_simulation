LATENCIES = {
    "LD": 2,
    "SD": 2,
    "ADDD": 2,
    "SUBD": 2,
    "MULTD": 10,
    "DIVD": 40
}

def execute_instruction(instruction, clock, register_result_status):
    if instruction.status == "issued" and instruction.execute_start is None:
        if instruction.op not in ["LD", "SD"]:
            if not can_execute(instruction, clock, register_result_status):
                return False  

        instruction.execute_start = clock
        instruction.execute_end = clock + LATENCIES[instruction.op]
        instruction.status = "executing"
        return True
    return False


def can_execute(inst, clock, register_result_status):
    if inst.status != "issued":
        return False

    if register_result_status.get(inst.src1) is not None:
        return False
    if register_result_status.get(inst.src2) is not None:
        return False

    return True