#!/bin/bash
# Chạy file log.py
echo "Starting log.py..."
python3 /home/linh/catkinws3/src/agv_multigoal/src/agv_multi_py/agv_multi_log.py &

sleep 5

echo "Starting move_bash.launch..."
roslaunch agv_navigation move_base.launch & 

sleep 10

# Chạy file run.py
echo "Starting draw.py..."
python3 /home/linh/catkinws3/src/agv_multigoal/src/agv_multi_py/agv_multi_draw.py &  # Dấu & để chạy nền (background)

sleep 5

#Chay file draw.py
echo "Starting run.py..."
python3 /home/linh/catkinws3/src/agv_multigoal/src/agv_multi_py/agv_multi_run.py &

# Đợi tất cả các process hoàn thành (tùy chọn)
wait

echo "All processes finished."