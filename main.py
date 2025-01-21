from instruction import Instruction
from reservation_station import init_reservation_stations
from load_store_buffers import init_load_store_buffers
from issue_instruction import issue_instruction
from execute import execute_instruction, can_execute
from write_back import write_result, complete_instruction
from print_state import print_state


reservation_stations = init_reservation_stations()
load_buffers, store_buffers = init_load_store_buffers()
register_result_status = {f"F{i}": None for i in range(0, 32, 2)}

instructions = [
    Instruction("LD", "F6", "34+R2", None),
    Instruction("LD", "F2", "45+R3", None),
    Instruction("MULTD", "F0", "F2", "F4"),
    Instruction("SUBD", "F8", "F6", "F2"),
    Instruction("DIVD", "F10", "F0", "F6"),
    Instruction("ADDD", "F6", "F8", "F2")
]

LATENCIES = {
    "LD": 2,
    "SD": 2,
    "ADDD": 2,
    "SUBD": 2,
    "MULTD": 10,
    "DIVD": 40
}


user_choice = input("Would you like to proceed step-by-step (s) or run the simulation to completion (c)? ")


clock = 1  
while any(inst.status not in ["completed", "writing"] for inst in instructions):
    for inst in instructions:
        if inst.status == "waiting":
            issued = issue_instruction(inst, clock, reservation_stations, load_buffers, store_buffers, register_result_status)
            if issued:
                break  
        elif inst.status == "issued" and can_execute(inst, clock, register_result_status):
            execute_instruction(inst, clock, register_result_status)
        elif inst.status == "executing":
            write_result(inst, clock, reservation_stations, load_buffers, store_buffers, register_result_status, instructions)
        elif inst.status == "writing":
            complete_instruction(inst, clock, reservation_stations, load_buffers, store_buffers, register_result_status)

    print_state(clock, instructions, reservation_stations, load_buffers, store_buffers, register_result_status)

    if user_choice.lower() == 's':
        input("Press Enter to proceed to the next clock cycle...")
    
    clock += 1

print("Simulation complete. ")