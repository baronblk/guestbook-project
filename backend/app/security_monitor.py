"""
Security Monitoring und Incident Response System
Überwacht und protokolliert Sicherheitsereignisse
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import asyncio

@dataclass
class SecurityEvent:
    """Sicherheitsereignis-Datenklasse"""
    timestamp: datetime
    event_type: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    source_ip: str
    user_agent: Optional[str]
    username: Optional[str]
    endpoint: Optional[str]
    details: Dict
    resolved: bool = False

class SecurityMonitor:
    """Security Event Monitor und Response System"""

    def __init__(self):
        self.events: deque = deque(maxlen=10000)  # Letzte 10k Events
        self.active_threats: Dict[str, List[SecurityEvent]] = defaultdict(list)
        self.blocked_ips: Dict[str, datetime] = {}

        # Konfiguration
        self.thresholds = {
            "failed_login_attempts": {"count": 5, "window": 300},  # 5 in 5 Minuten
            "rate_limit_violations": {"count": 10, "window": 60},   # 10 in 1 Minute
            "suspicious_patterns": {"count": 3, "window": 180}     # 3 in 3 Minuten
        }

        # Logger konfigurieren
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Security Logger konfigurieren"""
        logger = logging.getLogger("security_monitor")
        logger.setLevel(logging.INFO)

        # File Handler für persistente Logs
        file_handler = logging.FileHandler("/app/logs/security.log")
        file_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        return logger

    def log_event(
        self,
        event_type: str,
        severity: str,
        source_ip: str,
        details: Dict,
        user_agent: Optional[str] = None,
        username: Optional[str] = None,
        endpoint: Optional[str] = None
    ):
        """Sicherheitsereignis protokollieren"""
        event = SecurityEvent(
            timestamp=datetime.utcnow(),
            event_type=event_type,
            severity=severity,
            source_ip=source_ip,
            user_agent=user_agent,
            username=username,
            endpoint=endpoint,
            details=details
        )

        # Event speichern
        self.events.append(event)

        # Log schreiben
        self.logger.info(
            f"Security Event: {event_type} | "
            f"Severity: {severity} | "
            f"IP: {source_ip} | "
            f"User: {username or 'Anonymous'} | "
            f"Details: {json.dumps(details)}"
        )

        # Threat Detection
        self._analyze_threat_patterns(event)

    def _analyze_threat_patterns(self, event: SecurityEvent):
        """Bedrohungsmuster analysieren"""
        key = f"{event.source_ip}:{event.event_type}"

        # Event zu aktiven Bedrohungen hinzufügen
        self.active_threats[key].append(event)

        # Alte Events entfernen (außerhalb des Zeitfensters)
        threshold_config = self.thresholds.get(event.event_type, {"window": 300})
        cutoff_time = datetime.utcnow() - timedelta(seconds=threshold_config["window"])

        self.active_threats[key] = [
            e for e in self.active_threats[key]
            if e.timestamp > cutoff_time
        ]

        # Threshold prüfen
        threshold = self.thresholds.get(event.event_type, {"count": 5})
        if len(self.active_threats[key]) >= threshold["count"]:
            self._trigger_response(event.source_ip, event.event_type, self.active_threats[key])

    def _trigger_response(self, source_ip: str, event_type: str, events: List[SecurityEvent]):
        """Automatische Sicherheitsmaßnahmen auslösen"""
        self.logger.warning(
            f"SECURITY ALERT: Threshold exceeded for {event_type} from IP {source_ip}. "
            f"Events: {len(events)}"
        )

        # IP temporär blockieren
        block_duration = self._get_block_duration(event_type, len(events))
        self.blocked_ips[source_ip] = datetime.utcnow() + timedelta(seconds=block_duration)

        # Kritische Events
        if any(event.severity == "CRITICAL" for event in events):
            self._handle_critical_threat(source_ip, events)

    def _get_block_duration(self, event_type: str, event_count: int) -> int:
        """Block-Dauer basierend auf Event-Typ und -Anzahl berechnen"""
        base_duration = {
            "failed_login_attempts": 900,    # 15 Minuten
            "rate_limit_violations": 300,    # 5 Minuten
            "suspicious_patterns": 1800      # 30 Minuten
        }

        duration = base_duration.get(event_type, 600)

        # Eskalation bei wiederholten Verstößen
        if event_count > 10:
            duration *= 2
        if event_count > 20:
            duration *= 3

        return min(duration, 86400)  # Max 24 Stunden

    def _handle_critical_threat(self, source_ip: str, events: List[SecurityEvent]):
        """Kritische Bedrohungen behandeln"""
        self.logger.critical(
            f"CRITICAL SECURITY THREAT from IP {source_ip}. "
            f"Events: {len(events)}. Initiating enhanced response."
        )

        # Längere Blockierung für kritische Threats
        self.blocked_ips[source_ip] = datetime.utcnow() + timedelta(hours=24)

        # TODO: Weitere Maßnahmen wie E-Mail-Benachrichtigungen

    def is_ip_blocked(self, ip_address: str) -> bool:
        """Prüfen ob IP blockiert ist"""
        if ip_address in self.blocked_ips:
            if datetime.utcnow() < self.blocked_ips[ip_address]:
                return True
            else:
                # Block abgelaufen
                del self.blocked_ips[ip_address]
        return False

    def get_security_summary(self, hours: int = 24) -> Dict:
        """Security-Zusammenfassung der letzten X Stunden"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_events = [e for e in self.events if e.timestamp > cutoff_time]

        summary = {
            "total_events": len(recent_events),
            "events_by_type": defaultdict(int),
            "events_by_severity": defaultdict(int),
            "unique_ips": set(),
            "blocked_ips": len(self.blocked_ips),
            "critical_events": 0
        }

        for event in recent_events:
            summary["events_by_type"][event.event_type] += 1
            summary["events_by_severity"][event.severity] += 1
            summary["unique_ips"].add(event.source_ip)

            if event.severity == "CRITICAL":
                summary["critical_events"] += 1

        summary["unique_ips"] = len(summary["unique_ips"])

        return dict(summary)

    def get_recent_events(self, limit: int = 50) -> List[Dict]:
        """Letzte Security Events abrufen"""
        recent = list(self.events)[-limit:] if len(self.events) > limit else list(self.events)
        return [asdict(event) for event in reversed(recent)]

# Globale Monitor-Instanz
security_monitor = SecurityMonitor()

# Event-Helper-Funktionen
def log_failed_login(ip_address: str, username: str, user_agent: str = None):
    """Fehlgeschlagenen Login protokollieren"""
    security_monitor.log_event(
        event_type="failed_login_attempts",
        severity="MEDIUM",
        source_ip=ip_address,
        username=username,
        user_agent=user_agent,
        endpoint="/api/admin/login",
        details={"attempted_username": username}
    )

def log_rate_limit_violation(ip_address: str, endpoint: str, user_agent: str = None):
    """Rate Limit Verletzung protokollieren"""
    security_monitor.log_event(
        event_type="rate_limit_violations",
        severity="LOW",
        source_ip=ip_address,
        endpoint=endpoint,
        user_agent=user_agent,
        details={"exceeded_endpoint": endpoint}
    )

def log_suspicious_activity(ip_address: str, activity_type: str, details: Dict, user_agent: str = None):
    """Verdächtige Aktivität protokollieren"""
    security_monitor.log_event(
        event_type="suspicious_patterns",
        severity="HIGH",
        source_ip=ip_address,
        user_agent=user_agent,
        details={**details, "activity_type": activity_type}
    )

def log_successful_login(ip_address: str, username: str, user_agent: str = None):
    """Erfolgreichen Login protokollieren"""
    security_monitor.log_event(
        event_type="successful_login",
        severity="LOW",
        source_ip=ip_address,
        username=username,
        user_agent=user_agent,
        endpoint="/api/admin/login",
        details={"login_success": True}
    )
