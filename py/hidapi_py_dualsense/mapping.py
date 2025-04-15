

def get_trigger_feedback_active(in_report: InReport) -> bool:
    return bool(in_report.right_trigger_feedback & 0x10)


def get_trigger_feedback_value(in_report: InReport) -> int:
    return in_report.right_trigger_feedback & 0xff


def get_trigger_feedback(feedback_active: bool, feedback_value: int) -> TriggerFeedback:
    return TriggerFeedback(
        active=feedback_active,
        value=feedback_value
    )


def get_touch_finger_1_active(in_report: InReport) -> bool:
    return not (in_report.touch_1_0 & 0x80)


def get_touch_finger_1_id(in_report: InReport) -> int:
    return in_report.touch_1_0 & 0x7F


def get_touch_finger_1_x(in_report: InReport) -> int:
    return ((in_report.touch_1_2 & 0x0F) << 8) | in_report.touch_1_1


def get_touch_finger_1_y(in_report: InReport) -> int:
    return (in_report.touch_1_3 << 4) | ((in_report.touch_1_2 & 0xF0) >> 4)


def get_touch_finger_1(touch_finger_1_active: bool, touch_finger_1_id: int, touch_finger_1_x: int, touch_finger_1_y: int) -> TouchFinger:
    return TouchFinger(
        active=touch_finger_1_active,
        id=touch_finger_1_id,
        x=touch_finger_1_x,
        y=touch_finger_1_y,
    )


def get_orientation(orientation: Orientation, accelerometer: Accelerometer, gyroscope: Gyroscope, dt: float) -> Orientation:
    alpha: float = 0.98
    roll_acc = math.atan2(accelerometer.y, accelerometer.z)
    pitch_acc = math.atan2(-accelerometer.x,
                           math.sqrt(accelerometer.y**2 + accelerometer.z**2))

    roll = alpha * (orientation.roll + gyroscope.x * dt) + \
        (1 - alpha) * roll_acc
    pitch = alpha * (orientation.pitch + gyroscope.y * dt) + \
        (1 - alpha) * pitch_acc
    yaw = orientation.yaw + gyroscope.z * dt  # yaw only from gyro
    return Orientation(
        pitch=pitch,
        roll=roll,
        yaw=yaw
    )


def get_battery_level_percentage(in_report: InReport) -> float:
    batt_level_raw: int = in_report.battery_0 & 0x0f
    if batt_level_raw > 8:
        batt_level_raw = 8
    batt_level: float = batt_level_raw / 8
    return batt_level * 100


def get_battery_full(in_report: InReport) -> bool:
    return not not (in_report.battery_0 & 0x20)


def battery_charging(in_report: InReport) -> bool:
    return not not (in_report.battery_1 & 0x08)


def get_battery(battery_level_percentage: float, battery_full: bool, battery_charging: bool) -> Battery:
    return Battery(
        level_percentage=battery_level_percentage,
        full=battery_full,
        charging=battery_charging,
    )
