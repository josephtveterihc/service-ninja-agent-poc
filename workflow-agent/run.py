#!/usr/bin/env python3
"""
Setup and run script for the Service Monitoring Agent

Project Structure:
├── src/                                       # Production code
│   ├── service_monitoring_workflow.py           # Main monitoring workflow
│   ├── monitoring_tools.py                      # Service monitoring utilities
│   ├── document_tools.py                        # Documentation search utilities
│   ├── agent_instructions/                      # Agent behavior definitions
│   │   ├── detector_agent_instructions.md          # Issue detection agent
│   │   ├── analyzer_agent_instructions.md          # Analysis agent
│   │   ├── alerting_agent_instructions.md          # Alert management agent
│   │   └── info_agent_instructions.md              # Information agent
│   └── __init__.py
├── demo/                                      # Demo versions (no Azure needed)
│   ├── demo_monitoring_workflow.py              # Mock workflow demo
│   └── demo_monitoring_capabilities.py          # Monitoring tools demo
├── test/                                      # Test suite
│   └── test_monitoring_tools.py                 # Monitoring tools tests
└── run.py                                     # This file - easy launcher
"""

import sys
import os
import argparse
import subprocess

def run_main_workflow():
    """Run the main production workflow"""
    print("🚀 Starting Production Service Monitoring Workflow...")
    print("Note: Requires Azure credentials and proper endpoint configuration")
    # Run the workflow directly as a script to avoid import conflicts
    workflow_path = os.path.join(os.path.dirname(__file__), "src", "service_monitoring_workflow.py")
    subprocess.run([sys.executable, workflow_path])

def run_demo_workflow():
    """Run the demo workflow with mock responses"""
    print("🎭 Starting Demo Monitoring Workflow (No Azure required)...")
    subprocess.run([sys.executable, "demo/demo_monitoring_workflow.py"])

def run_monitoring_demo():
    """Run the monitoring capabilities demo"""
    print("📈 Starting Monitoring Capabilities Demo...")
    subprocess.run([sys.executable, "demo/demo_monitoring_capabilities.py"])

def run_document_demo():
    """Run the monitoring document search capabilities demo"""
    print("📄 Starting Monitoring Document Search Demo...")
    print("Note: Add monitoring documents to src/documents/ folder for testing")
    subprocess.run([sys.executable, "demo/demo_monitoring_capabilities.py"])

def run_tests():
    """Run all tests"""
    print("🧪 Running Tests...")
    subprocess.run([sys.executable, "test/test_monitoring_tools.py"])

def show_project_info():
    """Show project structure and information"""
    print("""
📁 Service Monitoring Agent Project Structure
==============================================

src/                                    # Main source code
├── service_monitoring_workflow.py     # Production workflow with AI agents
├── monitoring_tools.py                # Service monitoring utilities
├── document_tools.py                  # Documentation search utilities
└── __init__.py                        # Package initialization

demo/                                   # Demo applications  
├── demo_monitoring_workflow.py        # Mock workflow (no Azure needed)
└── demo_monitoring_capabilities.py    # Monitoring tools demonstration

test/                                   # Test files
└── test_monitoring_tools.py           # Monitoring tools tests

🚀 Available Commands:
- python run.py --workflow         # Run production workflow (requires Azure)
- python run.py --demo             # Run demo workflow (no Azure required)
- python run.py --monitor-demo      # Run monitoring capabilities demo
- python run.py --document-demo     # Run document search demo
- python run.py --test              # Run tests
- python run.py --info              # Show this information
""")

def main():
    parser = argparse.ArgumentParser(description="Service Monitoring Agent Runner")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--workflow', action='store_true', help='Run production workflow')
    group.add_argument('--demo', action='store_true', help='Run demo workflow')
    group.add_argument('--monitor-demo', action='store_true', help='Run monitoring capabilities demo')
    group.add_argument('--document-demo', action='store_true', help='Run document search demo')
    group.add_argument('--test', action='store_true', help='Run tests')
    group.add_argument('--info', action='store_true', help='Show project info')
    
    args = parser.parse_args()
    
    if args.workflow:
        run_main_workflow()
    elif args.demo:
        run_demo_workflow()
    elif args.monitor_demo:
        run_monitoring_demo()
    elif args.document_demo:
        run_document_demo()
    elif args.test:
        run_tests()
    elif args.info:
        show_project_info()

if __name__ == "__main__":
    main()