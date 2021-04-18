import can
import csv
import time
import math

filename = "test.blf"
log = can.BLFReader("test.blf")
log = list(log)

log_output = []

# message包含以下属性
# arbitration_id:199
# bitrate_switch:False
# channel:0
# data:bytearray(b'\x00\x00\x00\x00\x00\x00\x04\x04')
# dlc:8
# error_state_indicator:False
# id_type:False
# is_error_frame:False
# is_extended_id:False
# is_fd:False
# is_remote_frame:False
# timestamp:1617861021.10497

# str(message):
# 'Timestamp: 1617861021.104970        ID: 00c7    S                DLC:  8    00 00 00 00 00 00 04 04     Channel: 0'

time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(log[0].timestamp))
log_output.append([time, 'Channel', 'CAN / CAN FD', 'Frame Type', 'CAN ID(HEX)', 'DLC', 'Data(HEX)'])
for msg in log:
    time_secs = msg.timestamp - log[0].timestamp
    time_secs = '%f' % (time_secs)

    if msg.is_fd:
        can_fd = 'CAN FD'
    else:
        can_fd = 'CAN'
    if msg.bitrate_switch:
        can_fd = can_fd + ': Bitrate Switch'

    if msg.is_error_frame:
        frame_type = 'Error'
    elif msg.is_remote_frame:
        frame_type = 'Remote'
    else:
        frame_type = 'Data'

    if msg.is_extended_id:
        can_id = '0x{:08X}'.format(msg.arbitration_id)
    else:
        can_id = '0x{:03X}'.format(msg.arbitration_id)

    data = ''
    for byte in msg.data:
        data = data + '{:02X}'.format(byte) + ' '

    log_output.append([time_secs, msg.channel, can_fd, frame_type, can_id, msg.dlc, data])

with open("output.csv", "w", newline='') as f:
    writer = csv.writer(f, dialect='excel')
    writer.writerows(log_output)
