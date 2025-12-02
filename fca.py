from models import SOPRule

class FeedbackCoachingAgent:
    def __init__(self, rules: list[SOPRule]):
        self.rules = rules

    def ask(self, question: str):
        """
        Answers a natural language question based on SOP rules.
        """
        # Simple keyword matching for prototype
        question = question.lower()
        
        if "gear" in question:
            relevant_rules = [r for r in self.rules if "GEAR" in r.rule_id]
        elif "flaps" in question:
            relevant_rules = [r for r in self.rules if "FLAPS" in r.rule_id]
        else:
            relevant_rules = []

        if relevant_rules:
            response = "Here are the relevant procedures:\n"
            for r in relevant_rules:
                response += f"- {r.rule_id}: {r.required_action} (Condition: {r.pre_condition})\n"
            return response
        else:
            return "I couldn't find a specific procedure for that. Please check the SOP manual."
