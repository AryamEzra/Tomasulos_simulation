from execute import execute_instruction, can_execute

def issue_instruction(instruction, clock, reservation_stations, load_buffers, store_buffers, register_result_status):
    op = instruction.op
    if op == "LD":
        for buffer in load_buffers:
            if not buffer.busy:
                buffer.busy = True
                buffer.address = instruction.src1
                instruction.issue = clock
                instruction.status = "issued"
                register_result_status[instruction.dest] = f"Load{buffer.id}"  
                execute_instruction(instruction, clock, register_result_status)  
                return True

    elif op == "SD":
        for buffer in store_buffers:
            if not buffer.busy:
                buffer.busy = True
                buffer.address = instruction.src1
                instruction.issue = clock
                instruction.status = "issued"
                return True
    else:
        
        if op in ["ADDD", "SUBD"]:
            station_type = "Add"
        elif op in ["MULTD", "DIVD"]:
            station_type = "Mul"
        
        for station in reservation_stations[station_type]:
            if not station.busy:
                station.busy = True
                station.op = op
                station.dest = instruction.dest
                station.src1 = instruction.src1
                station.src2 = instruction.src2
                instruction.issue = clock
                instruction.status = "issued"
                
                
                if station.src1 in register_result_status and register_result_status[station.src1] is None:
                    station.src1 = instruction.src1
                if station.src2 in register_result_status and register_result_status[station.src2] is None:
                    station.src2 = instruction.src2

                register_result_status[instruction.dest] = f"{station_type}{station.id}"  
                return True
    return False

