from issue_instruction import issue_instruction
from execute import execute_instruction, can_execute
from write_back import write_result, complete_instruction

def print_state(clock, instructions, reservation_stations, load_buffers, store_buffers, register_result_status):
    print(f"\nClock Cycle: {clock}")
    print("Instruction Status:")
    print(f"{'Instruction':<10} {'Issue':<5} {'Execute Start':<15} {'Execute End':<12} {'Write Result':<12}")
    for inst in instructions:
        issue = str(inst.issue) if inst.issue is not None and inst.issue <= clock else "-"
        execute_start = str(inst.execute_start) if inst.execute_start is not None and inst.execute_start <= clock else "-"
        execute_end = str(inst.execute_end) if inst.execute_end is not None and inst.execute_end <= clock else "-"
        write_result = str(inst.write_result) if inst.write_result is not None and inst.write_result <= clock else "-"
        print(f"{inst.op:<10} {issue:<5} {execute_start:<15} {execute_end:<12} {write_result:<12}")

    print("\nReservation Stations:")
    print(f"{'Type':<5} {'ID':<2} {'Busy':<5} {'Op':<6} {'Dest':<5} {'Src1':<5} {'Src2':<5} ")
    for station_type, stations in reservation_stations.items():
        for station in stations:
            op = station.op if station.op is not None else "-"
            dest = station.dest if station.dest is not None else "-"
            src1 = station.src1 if station.src1 is not None else "-"
            src2 = station.src2 if station.src2 is not None else "-"
            
            print(f"{station.type:<5} {station.id:<2} {station.busy:<5} {op:<6} {dest:<5} {src1:<5} {src2:<5} ")
    
    print("\nLoad Buffers:")
    print(f"{'ID':<2} {'Busy':<5} {'Address':<10}")
    for buffer in load_buffers:
        address = buffer.address if buffer.address is not None else "-"
        print(f"{buffer.id:<2} {buffer.busy:<5} {address:<10}")

    print("\nStore Buffers:")
    print(f"{'ID':<2} {'Busy':<5} {'Address':<10}")
    for buffer in store_buffers:
        address = buffer.address if buffer.address is not None else "-"
        print(f"{buffer.id:<2} {buffer.busy:<5} {address:<10}")

    print("\nRegister Result Status:")
    registers = sorted(register_result_status.keys(), key=lambda x: int(x[1:]))  # Sort numerically
    print("  ".join(f"{reg}: {register_result_status[reg] if register_result_status[reg] else '-'}" for reg in registers))