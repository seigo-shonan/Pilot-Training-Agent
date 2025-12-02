from dataclasses import dataclass

@dataclass
class AircraftState:
    timestamp: float
    altitude: int
    airspeed: int
    engine_power_setting: float
    flaps_setting: int
    landing_gear_state: bool
    checklist_status: str

@dataclass
class SOPRule:
    rule_id: str
    pre_condition: str
    required_action: str
    time_limit_sec: float
    severity: int
