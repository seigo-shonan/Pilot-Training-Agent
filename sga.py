import json
from collections import Counter

class ScenarioGenerationAgent:
    def __init__(self):
        self.error_log_file = "PEA_Error_Log.json"
        self.scenario_file = "ScenarioInjection.json"

    def analyze_weakness(self):
        """
        Analyzes the error log to find weaknesses.
        """
        try:
            with open(self.error_log_file, 'r') as f:
                errors = json.load(f)
        except FileNotFoundError:
            return None

        if not errors:
            return "General_Review"

        rule_ids = [e.get('rule_id') for e in errors]
        most_common_violation = Counter(rule_ids).most_common(1)[0][0]
        
        print(f"[SGA] Identified Weakness: {most_common_violation}")
        return most_common_violation

    def generate_next_scenario(self, weakness_topic):
        """
        Generates the next scenario based on the weakness topic.
        """
        scenario_config = {
            "scenario_id": f"Training_{weakness_topic}",
            "conditions": {},
            "injections": []
        }

        if weakness_topic == "GEAR_CHECK":
            scenario_config["conditions"] = {"wind_speed": 15, "visibility": "low"}
            scenario_config["injections"].append({"type": "sensor_failure", "system": "landing_gear_indicator", "time": 60})
        elif weakness_topic == "FLAPS_TAKEOFF":
             scenario_config["conditions"] = {"runway_condition": "wet", "wind_direction": 270}
             scenario_config["injections"].append({"type": "distraction", "message": "ATC Traffic Alert", "time": 10})
        else:
             scenario_config["conditions"] = {"weather": "clear"}

        with open(self.scenario_file, 'w') as f:
            json.dump(scenario_config, f, indent=4)
        
        print(f"[SGA] Next Scenario Generated: {self.scenario_file}")
        print(json.dumps(scenario_config, indent=2))
