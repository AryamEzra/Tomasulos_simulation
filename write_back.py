# write_back.py
from execute import can_execute, execute_instruction

def write_result(instruction, clock, reservation_stations, load_buffers, store_buffers, register_result_status, instructions):
     # Ensure the write stage occurs in the cycle after execution ends
     if instruction.status == "executing" and (clock == instruction.execute_end + 1 or clock > instruction.execute_end + 1):
         instruction.write_result = instruction.execute_end + 1
         instruction.status = "writing"
 
         # Free the load/store buffer if LD/SD
         if instruction.op == "LD":
             for buffer in load_buffers:
                 if buffer.busy and buffer.address == instruction.src1:
                     buffer.busy = False
                     buffer.address = None
                     break
 
         elif instruction.op == "SD":
             for buffer in store_buffers:
                 if buffer.busy and buffer.address == instruction.src1:
                     buffer.busy = False
                     buffer.address = None
                     break
 
         # Free reservation stations for non-LD/SD instructions
         elif instruction.op not in ["LD", "SD"]:
             station_type = "Add" if instruction.op in ["ADDD", "SUBD"] else "Mul"
             for station in reservation_stations[station_type]:
                 if station.busy and station.dest == instruction.dest:
                     station.busy = False
                     station.op = None
                     station.dest = None
                     station.src1 = None
                     station.src2 = None
                     station.execute_start = None
                     station.execute_end = None
                     station.temp1 = None
                     station.temp2 = None
                     break
 
         # Free the destination register
         register_result_status[instruction.dest] = None

         
         for station_type in ["Add", "Mul"]:
             for station in reservation_stations[station_type]:
                 if station.busy:
 
                     if station.temp1 == instruction.dest:
                         station.src1 = instruction.dest
                         station.temp1 = None
                     if station.temp2 == instruction.dest:
                         station.src2 = instruction.dest
                         station.temp2 = None
         
         for inst in instructions:
           if inst.status == "issued" and inst.op not in ["LD", "SD"]:
                 if can_execute(inst, clock, register_result_status, reservation_stations):
                     execute_instruction(inst, clock, register_result_status, reservation_stations)

         return True
     return False

def complete_instruction(inst, clock, reservation_stations, load_buffers, store_buffers, register_result_status):
     inst.is_complete = True
     inst.complete_time = clock
     
     if inst.status == "writing":
         inst.write_result = inst.execute_end +1

     inst.status = "completed"


     if inst.op in ["LD", "SD"]:
         buffers = load_buffers if inst.op == "LD" else store_buffers
         for buffer in buffers:
             if buffer.busy and buffer.address == inst.src1:
                 buffer.busy = False
                 buffer.address = None
                 break
     else:
         station_type = "Add" if inst.op in ["ADDD", "SUBD"] else "Mul"
         for station in reservation_stations[station_type]:
             if station.busy and station.dest == inst.dest:
                 station.busy = False
                 station.op = None
                 station.dest = None
                 station.src1 = None
                 station.src2 = None
                 station.execute_start = None
                 station.execute_end = None
                 station.temp1 = None
                 station.temp2 = None
                 break

     register_result_status[inst.dest] = None

     for station_type in ["Add", "Mul"]:
         for inst_in_wait in reservation_stations[station_type]:

             if inst_in_wait.busy:
                 if inst_in_wait.temp1 == inst.dest:
                   inst_in_wait.src1 = inst.dest
                   inst_in_wait.temp1 = None

                 if inst_in_wait.temp2 == inst.dest:
                   inst_in_wait.src2 = inst.dest
                   inst_in_wait.temp2 = None

     if inst.op in ["LD", "SD"]:
         for buffer in load_buffers + store_buffers:
             if buffer.busy and (buffer.address == inst.src1 or buffer.address == inst.src2):
                 buffer.busy = False
                 buffer.address = None
                 break