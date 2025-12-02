from dataclasses import dataclass

@dataclass
class AircraftState:
    timestamp: float
    altitude: float
    airspeed: float
    vertical_speed: float  # 追加
    heading: float         # 追加
    landing_gear_state: bool
    flaps_setting: int

@dataclass
class SOPRule:
    rule_id: str
    pre_condition: str
    required_action: str
    time_limit_sec: float
    severity: int
