class BaseScanner:
    """
    Abstract Base Class for all diagnostic scanning modules.
    Ensures structural consistency across V5 modules.
    """
    def __init__(self, name, category):
        self.name = name
        self.category = category  # e.g., "Firewall", "CPU"
        self.risk_penalty = 0
        self.findings = []

    def run(self):
        raise NotImplementedError("Scanners must implement their own run() method.")

    def get_results(self):
        return {
            "scanner": self.name,
            "category": self.category,
            "penalty": self.risk_penalty,
            "findings": self.findings
        }