#!/usr/bin/env python3
"""
Security Testing Script
Testet die implementierten Sicherheitsfeatures des Gästebuch-Systems
"""

import requests
import json
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class SecurityTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []

    def log_result(self, test_name: str, success: bool, details: str):
        """Test-Ergebnis protokollieren"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "test": test_name,
            "success": success,
            "details": details
        }
        self.results.append(result)
        status = "✅" if success else "❌"
        print(f"{status} {test_name}: {details}")

    def test_rate_limiting(self):
        """Rate Limiting testen"""
        print("\n🔒 Testing Rate Limiting...")

        # Schnelle Requests senden
        url = f"{self.base_url}/api/admin/login"
        payload = {"username": "test", "password": "test"}

        blocked = False
        for i in range(12):  # Mehr als das Limit
            try:
                response = self.session.post(url, json=payload, timeout=5)
                if response.status_code == 429:
                    blocked = True
                    self.log_result("Rate Limiting", True, f"Blocked after {i+1} requests")
                    break
            except Exception as e:
                self.log_result("Rate Limiting", False, f"Error: {str(e)}")
                return

        if not blocked:
            self.log_result("Rate Limiting", False, "Not blocked after 12 requests")

    def test_brute_force_protection(self):
        """Brute-Force-Schutz testen"""
        print("\n🔒 Testing Brute Force Protection...")

        url = f"{self.base_url}/api/admin/login"

        # Verschiedene falsche Passwörter versuchen
        for i in range(6):  # Mehr als das Limit von 5
            payload = {"username": "admin", "password": f"wrong_password_{i}"}

            try:
                response = self.session.post(url, json=payload, timeout=5)

                if response.status_code == 429:
                    self.log_result("Brute Force Protection", True, f"Account blocked after {i+1} attempts")
                    return
                elif response.status_code != 401:
                    self.log_result("Brute Force Protection", False, f"Unexpected response: {response.status_code}")
                    return

            except Exception as e:
                self.log_result("Brute Force Protection", False, f"Error: {str(e)}")
                return

        self.log_result("Brute Force Protection", False, "Not blocked after 6 failed attempts")

    def test_concurrent_login_attempts(self):
        """Parallele Login-Versuche testen"""
        print("\n🔒 Testing Concurrent Login Attempts...")

        def make_login_attempt(attempt_id):
            try:
                url = f"{self.base_url}/api/admin/login"
                payload = {"username": "admin", "password": f"wrong_{attempt_id}"}
                response = requests.post(url, json=payload, timeout=5)
                return response.status_code
            except Exception as e:
                return str(e)

        # 10 parallele Versuche
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_login_attempt, i) for i in range(10)]
            results = [future.result() for future in as_completed(futures)]

        # Prüfen ob Rate Limiting greift
        blocked_count = sum(1 for r in results if r == 429)

        if blocked_count > 0:
            self.log_result("Concurrent Login Attempts", True, f"{blocked_count}/10 requests blocked")
        else:
            self.log_result("Concurrent Login Attempts", False, "No requests blocked")

    def test_security_headers(self):
        """Sicherheits-Headers testen"""
        print("\n🔒 Testing Security Headers...")

        try:
            response = self.session.get(f"{self.base_url}/health")
            headers = response.headers

            required_headers = {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "X-XSS-Protection": "1; mode=block",
                "Referrer-Policy": "strict-origin-when-cross-origin",
                "Content-Security-Policy": lambda v: "default-src 'self'" in v
            }

            missing_headers = []
            for header, expected in required_headers.items():
                if header not in headers:
                    missing_headers.append(header)
                elif callable(expected) and not expected(headers[header]):
                    missing_headers.append(f"{header} (incorrect value)")
                elif not callable(expected) and headers[header] != expected:
                    missing_headers.append(f"{header} (incorrect value)")

            if missing_headers:
                self.log_result("Security Headers", False, f"Missing/incorrect: {', '.join(missing_headers)}")
            else:
                self.log_result("Security Headers", True, "All required headers present")

        except Exception as e:
            self.log_result("Security Headers", False, f"Error: {str(e)}")

    def test_jwt_token_validation(self):
        """JWT Token Validierung testen"""
        print("\n🔒 Testing JWT Token Validation...")

        # Ungültigen Token testen
        headers = {"Authorization": "Bearer invalid_token_here"}

        try:
            response = self.session.get(f"{self.base_url}/api/admin/reviews", headers=headers)

            if response.status_code == 401:
                self.log_result("JWT Token Validation", True, "Invalid token correctly rejected")
            else:
                self.log_result("JWT Token Validation", False, f"Invalid token accepted (status: {response.status_code})")

        except Exception as e:
            self.log_result("JWT Token Validation", False, f"Error: {str(e)}")

    def test_input_validation(self):
        """Input-Validierung testen"""
        print("\n🔒 Testing Input Validation...")

        # SQL Injection Versuche
        sql_payloads = [
            "'; DROP TABLE reviews; --",
            "admin' OR '1'='1",
            "1' UNION SELECT * FROM admin_users --"
        ]

        for payload in sql_payloads:
            try:
                url = f"{self.base_url}/api/admin/login"
                data = {"username": payload, "password": "test"}
                response = self.session.post(url, json=data, timeout=5)

                # Server sollte nicht crashen und strukturierte Antwort geben
                if response.status_code in [400, 401, 422]:
                    continue  # Erwartete Fehler
                else:
                    self.log_result("Input Validation", False, f"Unexpected response to SQL injection: {response.status_code}")
                    return

            except Exception as e:
                self.log_result("Input Validation", False, f"Error with payload '{payload}': {str(e)}")
                return

        self.log_result("Input Validation", True, "SQL injection attempts properly handled")

    def test_cors_configuration(self):
        """CORS-Konfiguration testen"""
        print("\n🔒 Testing CORS Configuration...")

        try:
            # Preflight-Request simulieren
            headers = {
                "Origin": "http://malicious-site.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }

            response = self.session.options(f"{self.base_url}/api/admin/login", headers=headers)

            # Prüfen ob CORS restrictiv konfiguriert ist
            cors_origin = response.headers.get("Access-Control-Allow-Origin")

            if cors_origin == "*":
                self.log_result("CORS Configuration", False, "Allows all origins (*)")
            elif cors_origin and "malicious-site.com" in cors_origin:
                self.log_result("CORS Configuration", False, "Allows malicious origin")
            else:
                self.log_result("CORS Configuration", True, "CORS properly restricted")

        except Exception as e:
            self.log_result("CORS Configuration", False, f"Error: {str(e)}")

    def run_all_tests(self):
        """Alle Sicherheitstests ausführen"""
        print("🛡️  Starting Security Test Suite")
        print("=" * 50)

        test_methods = [
            self.test_security_headers,
            self.test_rate_limiting,
            self.test_brute_force_protection,
            self.test_jwt_token_validation,
            self.test_input_validation,
            self.test_cors_configuration,
            self.test_concurrent_login_attempts
        ]

        for test_method in test_methods:
            try:
                test_method()
                time.sleep(1)  # Kurze Pause zwischen Tests
            except Exception as e:
                print(f"❌ Test {test_method.__name__} failed: {str(e)}")

        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)

        passed = sum(1 for r in self.results if r["success"])
        total = len(self.results)

        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")

        # Detaillierte Ergebnisse speichern
        with open("security_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"\n📝 Detailed results saved to: security_test_results.json")

def main():
    """Hauptfunktion"""
    import argparse

    parser = argparse.ArgumentParser(description="Security Testing für Gästebuch-System")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL der API")
    parser.add_argument("--test", help="Einzelnen Test ausführen")

    args = parser.parse_args()

    tester = SecurityTester(args.url)

    if args.test:
        test_method = getattr(tester, f"test_{args.test}", None)
        if test_method:
            test_method()
        else:
            print(f"Test '{args.test}' not found")
    else:
        tester.run_all_tests()

if __name__ == "__main__":
    main()
