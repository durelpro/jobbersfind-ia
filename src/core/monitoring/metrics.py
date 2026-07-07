"""
JITSE AI Operations — Metrics et Monitoring.

Surveillance des performances opérationnelles de l'IA (Volume 6).
"""

class AIMonitoring:
    """
    Mesure la latence, le nombre de fraudes détectées par jour,
    et le taux de rejet par métier pour monitorer le Drift.
    """
    
    def __init__(self):
        # Stats en mémoire pour la simulation
        self.stats = {
            "total_requests": 0,
            "total_frauds_detected": 0,
            "average_latency_ms": 0.0
        }
        
    def record_request(self, latency_ms: float, fraud_detected: bool):
        """Enregistre les métriques brutes d'une inférence."""
        # Calcul de moyenne glissante simulée
        current_reqs = self.stats["total_requests"]
        new_total = current_reqs + 1
        
        self.stats["average_latency_ms"] = (
            (self.stats["average_latency_ms"] * current_reqs) + latency_ms
        ) / new_total
        
        self.stats["total_requests"] = new_total
        if fraud_detected:
            self.stats["total_frauds_detected"] += 1
            
    def generate_health_report(self) -> dict:
        return self.stats

global_ai_monitor = AIMonitoring()
