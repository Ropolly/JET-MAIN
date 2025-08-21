"""
Base test utilities for API endpoint testing.
Tests are designed to run against a live server.
"""
import json
import requests
import sys
from typing import Dict, Any, Optional


class APITester:
    """Base class for testing API endpoints against a running server."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000", auth_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        if auth_token:
            self.session.headers.update({
                'Authorization': f'Bearer {auth_token}'
            })
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate with the API and store the token."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/token/",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('access') or data.get('token')
                if token:
                    self.session.headers.update({
                        'Authorization': f'Bearer {token}'
                    })
                    return True
            return False
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def print_response(self, response: requests.Response, title: str):
        """Print formatted response details."""
        print(f"\n{'='*60}")
        print(f"TEST: {title}")
        print(f"{'='*60}")
        print(f"URL: {response.request.method} {response.url}")
        print(f"Status Code: {response.status_code}")
        
        if response.request.body:
            print(f"Request Body: {response.request.body}")
        
        try:
            response_data = response.json()
            print(f"Response Body:")
            print(json.dumps(response_data, indent=2))
        except:
            print(f"Response Body (raw): {response.text}")
        
        print(f"{'='*60}\n")
    
    def check_no_id_fields(self, data: Any, path: str = "") -> list:
        """Check for _id fields in response data and return violations."""
        violations = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                # Check for _id fields (but allow 'id' itself)
                if key.endswith('_id') and key != 'id':
                    violations.append(f"Found _id field '{key}' at path '{current_path}'")
                violations.extend(self.check_no_id_fields(value, current_path))
        elif isinstance(data, list):
            for i, item in enumerate(data):
                violations.extend(self.check_no_id_fields(item, f"{path}[{i}]"))
        
        return violations
    
    def test_endpoint(self, endpoint: str, method: str = "GET", data: Dict = None, 
                     expect_status: int = 200, title: str = None) -> requests.Response:
        """Test an endpoint and print results."""
        url = f"{self.base_url}{endpoint}"
        title = title or f"{method} {endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "PATCH":
                response = self.session.patch(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            self.print_response(response, title)
            
            # Check for _id fields in GET responses
            if method.upper() == "GET" and response.status_code == 200:
                try:
                    response_data = response.json()
                    violations = self.check_no_id_fields(response_data)
                    if violations:
                        print("⚠️  _ID FIELD VIOLATIONS FOUND:")
                        for violation in violations:
                            print(f"   - {violation}")
                    else:
                        print("✅ No _id fields found in response")
                except:
                    pass
            
            # Check status code
            if response.status_code == expect_status:
                print(f"✅ Status code matches expected: {expect_status}")
            else:
                print(f"❌ Status code {response.status_code} != expected {expect_status}")
            
            return response
            
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None


def main():
    """Run basic connectivity test."""
    tester = APITester()
    
    print("Testing API connectivity...")
    response = tester.test_endpoint("/api/", title="API Root Connectivity Test")
    
    if response and response.status_code < 500:
        print("✅ API server is reachable")
    else:
        print("❌ API server is not reachable")
        sys.exit(1)


if __name__ == "__main__":
    main()
