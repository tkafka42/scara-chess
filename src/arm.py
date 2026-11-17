import chess

import kinematics as kin
import servo_settings as servo
from move_planner import BOX, RESERVE

BOX_XY = (45.0, 5.0)
RESERVE_XY = (5.0, 45.0)


def location_to_xy(location):
    if location == BOX:
        return BOX_XY
    if location == RESERVE:
        return RESERVE_XY
    file = chess.square_file(location)
    rank = chess.square_rank(location)
    return kin.square_to_xy(file, rank)


def location_to_servo_angles(location):
    x, y = location_to_xy(location)
    theta1, theta2 = kin.inverse_kinematics(x, y)
    shoulder = servo.joint_to_servo_angle("shoulder", theta1)
    elbow = servo.joint_to_servo_angle("elbow", theta2)
    return shoulder, elbow


def move_piece(from_location, to_location):
    from_shoulder, from_elbow = location_to_servo_angles(from_location)
    to_shoulder, to_elbow = location_to_servo_angles(to_location)
    print(f"pick  at shoulder {from_shoulder:.1f}, elbow {from_elbow:.1f}")
    print(f"place at shoulder {to_shoulder:.1f}, elbow {to_elbow:.1f}")


if __name__ == "__main__":
    move_piece(chess.E2, chess.E4)
    move_piece(chess.D5, BOX)
