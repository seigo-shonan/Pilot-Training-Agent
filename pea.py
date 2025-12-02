import json
import time
from models import AircraftState, SOPRule

class PerformanceEvaluationAgent:
    def __init__(self):
        self.error_log = []
        self.error_log_file = "PEA_Error_Log.json"

    def evaluate_sop(self, state: AircraftState, rules: list[SOPRule]):
        """
        Evaluates the current aircraft state against SOP rules.
        """
        for rule in rules:
            # Simplified rule checking logic for prototype
            # In a real system, this would involve complex state machine or logic parsing
            violation = False
            
            # Example logic: If gear is up but altitude is low (landing phase assumption)
            if rule.rule_id == "GEAR_CHECK" and state.altitude < 500 and not state.landing_gear_state:
                 violation = True
            
            # Example logic: Flaps not set for takeoff
            if rule.rule_id == "FLAPS_TAKEOFF" and state.altitude < 1000 and state.airspeed < 150 and state.flaps_setting == 0:
                violation = True

            if violation:
                error_entry = {
                    'error_type': 'SOP_VIOLATION',
                    'rule_id': rule.rule_id,
                    'timestamp': state.timestamp,
                    'severity': rule.severity,
                    'details': f"Violation of {rule.rule_id} at alt={state.altitude}, speed={state.airspeed}"
                }
                self.error_log.append(error_entry)
                self._log_error(error_entry)
                print(f"[PEA] Violation Detected: {error_entry['details']}")

    def _log_error(self, error_entry):
        try:
            with open(self.error_log_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        data.append(error_entry)
        
        with open(self.error_log_file, 'w') as f:
            json.dump(data, f, indent=4)

    def generate_feedback_report(self):
        """
        Generates an HTML report from the error log.
        """
        try:
            with open(self.error_log_file, 'r') as f:
                errors = json.load(f)
        except FileNotFoundError:
            errors = []

        html_content = "<html><body><h1>Pilot Training Feedback Report</h1>"
        html_content += f"<p>Total Violations: {len(errors)}</p>"
        html_content += "<table border='1'><tr><th>Time</th><th>Rule</th><th>Severity</th><th>Details</th></tr>"
        
        for error in errors:
            html_content += f"<tr><td>{error.get('timestamp')}</td><td>{error.get('rule_id')}</td><td>{error.get('severity')}</td><td>{error.get('details')}</td></tr>"
        
        html_content += "</table></body></html>"
        
        with open("FeedbackReport.html", "w") as f:
            f.write(html_content)
        print("[PEA] Feedback Report Generated: FeedbackReport.html")
