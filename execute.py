# execute.py

LATENCIES = {
    "LD": 2,
    "SD": 2,
    "ADDD": 2,
    "SUBD": 2,
    "MULTD": 10,
    "DIVD": 40
}

def execute_instruction(instruction, clock, register_result_status, reservation_stations):
    if instruction.status == "issued" and instruction.execute_start is None:
        if instruction.op not in ["LD", "SD"]:
            if not can_execute(instruction, clock, register_result_status, reservation_stations):
                return False

        instruction.execute_start = clock
        instruction.execute_end = clock + LATENCIES[instruction.op]
        instruction.status = "executing"
        return True
    return False


def can_execute(inst, clock, register_result_status, reservation_stations):
    if inst.status != "issued":
        return False

    if inst.op in ["LD", "SD"]:
        return True

    station_type = "Add" if inst.op in ["ADDD", "SUBD"] else "Mul"

    for station in reservation_stations[station_type]:
        if station.busy and station.dest == inst.dest:
            if station.temp1 or station.temp2:
                    return False
            else:
                    return True
    return False