"""
MCP Server debugging utilities
"""
import httpx
import json
import asyncio


async def test_mcp_server_health():
    """Test if MCP server is running and responding correctly"""
    print("🔍 Testing MCP Server Health...")
    print("=" * 50)
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Test 1: Check if server is running
            print("1️⃣ Testing server connectivity...")
            try:
                response = await client.get("http://localhost:3000/health")
                print(f"✅ Server is running (Status: {response.status_code})")
                if response.status_code == 200:
                    health_data = response.json()
                    print(f"📊 Health Data: {json.dumps(health_data, indent=2)}")
            except Exception as e:
                print(f"❌ Health check failed: {e}")
            
            # Test 2: Check tools listing
            print("\n2️⃣ Testing tools listing...")
            try:
                response = await client.get("http://localhost:3000/mcp/tools")
                print(f"📋 Tools endpoint status: {response.status_code}")
                if response.status_code == 200:
                    tools_data = response.json()
                    print(f"🔧 Available tools: {len(tools_data.get('tools', []))}")
                    for tool in tools_data.get('tools', [])[:3]:  # Show first 3 tools
                        print(f"  - {tool.get('name', 'unknown')}: {tool.get('description', 'no description')}")
            except Exception as e:
                print(f"❌ Tools listing failed: {e}")
            
            # Test 3: Test simple tool call
            print("\n3️⃣ Testing list_projects tool call...")
            try:
                response = await client.post(
                    "http://localhost:3000/mcp/tool/call",
                    json={
                        "name": "list_projects",
                        "arguments": {}
                    },
                    headers={"Content-Type": "application/json"}
                )
                print(f"📞 Tool call status: {response.status_code}")
                print(f"📄 Response headers: {dict(response.headers)}")
                print(f"📝 Raw response: {response.text[:500]}...")
                
                if response.text.strip():
                    try:
                        result = response.json()
                        print(f"✅ JSON parsed successfully")
                        print(f"🏗️ Response structure: {json.dumps(result, indent=2)}")
                    except json.JSONDecodeError as json_err:
                        print(f"❌ JSON parse error: {json_err}")
                else:
                    print("❌ Empty response received")
                    
            except Exception as e:
                print(f"❌ Tool call failed: {e}")
                
    except Exception as e:
        print(f"💥 Overall test failed: {e}")


async def test_mcp_capabilities():
    """Test MCP server capabilities endpoint"""
    print("\n🎯 Testing MCP Capabilities...")
    print("=" * 50)
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:3000/mcp/capabilities")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                capabilities = response.json()
                print(f"Capabilities: {json.dumps(capabilities, indent=2)}")
            else:
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"Error testing capabilities: {e}")


if __name__ == "__main__":
    asyncio.run(test_mcp_server_health())
    asyncio.run(test_mcp_capabilities())