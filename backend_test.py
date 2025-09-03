#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Coder Buddy Dashboard
Tests all API endpoints with both technical and general questions/requests
"""

import requests
import sys
import json
import time
from datetime import datetime

class CoderBuddyAPITester:
    def __init__(self, base_url="https://32766f6b-2244-4c6f-889f-e9060372d37d.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.session_timeout = 30  # seconds to wait for AI responses

    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED")
        
        if details:
            print(f"   Details: {details}")
        print()

    def test_health_check(self):
        """Test the health check endpoint"""
        print("🔍 Testing Health Check Endpoint...")
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy" and "service" in data:
                    self.log_test("Health Check", True, f"Status: {data['status']}, Service: {data['service']}")
                    return True
                else:
                    self.log_test("Health Check", False, f"Unexpected response format: {data}")
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
        return False

    def test_qa_technical_question(self):
        """Test Q&A with a technical programming question"""
        print("🔍 Testing Q&A - Technical Question...")
        try:
            question = "How do I use async/await in JavaScript?"
            payload = {
                "question": question,
                "context": ""
            }
            
            response = requests.post(
                f"{self.base_url}/api/ask-question", 
                json=payload, 
                timeout=self.session_timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if (data.get("success") and 
                    "answer" in data and 
                    data.get("question") == question and
                    len(data["answer"]) > 50):  # Reasonable answer length
                    
                    is_technical = data.get("is_technical", False)
                    self.log_test("Q&A Technical Question", True, 
                                f"Technical: {is_technical}, Answer length: {len(data['answer'])} chars")
                    return True
                else:
                    self.log_test("Q&A Technical Question", False, f"Invalid response: {data}")
            else:
                self.log_test("Q&A Technical Question", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Q&A Technical Question", False, f"Exception: {str(e)}")
        return False

    def test_qa_general_question(self):
        """Test Q&A with a general knowledge question"""
        print("🔍 Testing Q&A - General Question...")
        try:
            question = "What is artificial intelligence?"
            payload = {
                "question": question,
                "context": ""
            }
            
            response = requests.post(
                f"{self.base_url}/api/ask-question", 
                json=payload, 
                timeout=self.session_timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if (data.get("success") and 
                    "answer" in data and 
                    data.get("question") == question and
                    len(data["answer"]) > 50):
                    
                    is_technical = data.get("is_technical", False)
                    self.log_test("Q&A General Question", True, 
                                f"Technical: {is_technical}, Answer length: {len(data['answer'])} chars")
                    return True
                else:
                    self.log_test("Q&A General Question", False, f"Invalid response: {data}")
            else:
                self.log_test("Q&A General Question", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Q&A General Question", False, f"Exception: {str(e)}")
        return False

    def test_project_generation(self):
        """Test project generation with a simple request"""
        print("🔍 Testing Project Generation...")
        try:
            prompt = "Create a simple contact form with HTML, CSS, and JavaScript"
            payload = {
                "prompt": prompt
            }
            
            print(f"   Generating project with prompt: '{prompt}'")
            print("   ⏳ This may take 30-60 seconds for AI processing...")
            
            response = requests.post(
                f"{self.base_url}/api/generate-project", 
                json=payload, 
                timeout=60  # Longer timeout for project generation
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "result" in data:
                    session_info = data.get("session_info", {})
                    self.log_test("Project Generation", True, 
                                f"Message: {data.get('message', 'N/A')}, Session: {session_info.get('session_id', 'N/A')[:8]}...")
                    return True
                else:
                    self.log_test("Project Generation", False, f"Invalid response: {data}")
            else:
                self.log_test("Project Generation", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Project Generation", False, f"Exception: {str(e)}")
        return False

    def test_sessions_endpoint(self):
        """Test sessions monitoring endpoint"""
        print("🔍 Testing Sessions Endpoint...")
        try:
            response = requests.get(f"{self.base_url}/api/sessions", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "sessions" in data:
                    sessions = data["sessions"]
                    self.log_test("Sessions Endpoint", True, 
                                f"Found {len(sessions)} sessions")
                    return True
                else:
                    self.log_test("Sessions Endpoint", False, f"Invalid response format: {data}")
            else:
                self.log_test("Sessions Endpoint", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Sessions Endpoint", False, f"Exception: {str(e)}")
        return False

    def test_generated_projects_endpoint(self):
        """Test generated projects gallery endpoint"""
        print("🔍 Testing Generated Projects Endpoint...")
        try:
            response = requests.get(f"{self.base_url}/api/generated-projects", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "projects" in data:
                    projects = data["projects"]
                    self.log_test("Generated Projects Endpoint", True, 
                                f"Found {len(projects)} projects")
                    return True
                else:
                    self.log_test("Generated Projects Endpoint", False, f"Invalid response format: {data}")
            else:
                self.log_test("Generated Projects Endpoint", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Generated Projects Endpoint", False, f"Exception: {str(e)}")
        return False

    def test_root_endpoint(self):
        """Test root endpoint"""
        print("🔍 Testing Root Endpoint...")
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_test("Root Endpoint", True, f"Message: {data['message']}")
                    return True
                else:
                    self.log_test("Root Endpoint", False, f"Unexpected response: {data}")
            else:
                self.log_test("Root Endpoint", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Exception: {str(e)}")
        return False

    def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting Coder Buddy Backend API Tests")
        print("=" * 60)
        print(f"🌐 Testing against: {self.base_url}")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()

        # Test basic connectivity first
        if not self.test_health_check():
            print("❌ Health check failed - stopping tests")
            return False

        # Test all endpoints
        self.test_root_endpoint()
        self.test_qa_technical_question()
        self.test_qa_general_question()
        self.test_sessions_endpoint()
        self.test_generated_projects_endpoint()
        
        # Test project generation last (takes longest)
        self.test_project_generation()

        # Print summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Tests Passed: {self.tests_passed}/{self.tests_run}")
        print(f"❌ Tests Failed: {self.tests_run - self.tests_passed}/{self.tests_run}")
        
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 Backend API tests mostly successful!")
            return True
        else:
            print("⚠️  Backend API has significant issues that need attention")
            return False

def main():
    """Main test execution"""
    tester = CoderBuddyAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())