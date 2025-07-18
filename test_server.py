#!/usr/bin/env python3
"""
Simple test script to verify the MER Calculator server is working
"""

import urllib.request
import urllib.error
import json

def test_server():
    """Test the MER Calculator server."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing MER Calculator Server")
    print("=" * 50)
    
    # Test 1: Main page
    try:
        print("1. Testing main page...")
        response = urllib.request.urlopen(f"{base_url}/")
        if response.getcode() == 200:
            content = response.read().decode('utf-8')
            if "MER Calculator" in content:
                print("   ✅ Main page loads correctly")
                print(f"   📄 Page size: {len(content)} characters")
            else:
                print("   ❌ Main page content incorrect")
        else:
            print(f"   ❌ Wrong status code: {response.getcode()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: API defaults
    try:
        print("2. Testing API defaults...")
        response = urllib.request.urlopen(f"{base_url}/api/defaults")
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            if 'config' in data and 'user_inputs' in data:
                print("   ✅ API defaults working correctly")
                print(f"   📊 Default revenue: €{data['user_inputs']['target_revenue']:,}")
                print(f"   📈 Default MER: {data['user_inputs']['target_mer']}")
            else:
                print("   ❌ API response format incorrect")
        else:
            print(f"   ❌ Wrong status code: {response.getcode()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: API calculation
    try:
        print("3. Testing API calculation...")
        test_data = {
            "target_revenue": 820000,
            "target_mer": 7.5,
            "variable_cost": 0.65,
            "contribution_margin_goal": 176000,
            "revenue_increment": 20000
        }
        
        req = urllib.request.Request(
            f"{base_url}/api/calculate",
            data=json.dumps(test_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('success'):
                print("   ✅ API calculation working correctly")
                print(f"   💰 Contribution Margin: €{result['contribution_margin']:,.0f}")
                print(f"   🎯 Meets Goal: {result['meets_goal']}")
            else:
                print(f"   ❌ Calculation failed: {result.get('errors', 'Unknown error')}")
        else:
            print(f"   ❌ Wrong status code: {response.getcode()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🌐 Server Status: RUNNING")
    print("🔗 Access URL: http://localhost:8000")
    print("📱 Mobile Access: http://[your-ip]:8000")
    print("🛑 Stop server: Press Ctrl+C in the terminal")
    
    print("\n💡 Troubleshooting Tips:")
    print("• Make sure you're using http:// not https://")
    print("• Try refreshing the page (Ctrl+F5)")
    print("• Check if port 8000 is blocked by firewall")
    print("• Try a different browser")
    print("• Clear browser cache and cookies")

if __name__ == "__main__":
    test_server()