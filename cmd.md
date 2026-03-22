python inference.py \
    --input_path examples/videos/robot.mp4 \
    --trajectory tilt_up \
    --prompt "A two-arm robot assembles parts in front of a table." \
    --output_path outputs/tilt_up.mp4


python inference.py \
    --input_path /workspace/VerseCrafter/demo_data/my4/a.png \
    --static_scene \
    --trajectory move_right \
    --output_path outputs/move_right.mp4