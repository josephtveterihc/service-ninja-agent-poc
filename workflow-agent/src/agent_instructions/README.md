# Agent Instructions - README

This folder contains the instruction files for each AI agent in the PTO workflow system.

## Agent Files:

### 🧑‍💼 `employee_agent_instructions.md`
Instructions for the Employee Agent that helps format time-off requests.
- **Role**: Format and validate employee requests
- **Key Features**: Date calculation, request formatting
- **Tools**: Date utilities for relative date processing

### 👔 `manager_agent_instructions.md`
Instructions for the Manager Agent that reviews and approves requests.
- **Role**: Review requests and make approval decisions
- **Key Features**: Business logic, decision reasoning
- **Tools**: Date utilities for business day calculations

### 📧 `notification_agent_instructions.md`
Instructions for the Notification Agent that communicates decisions.
- **Role**: Generate professional status notifications
- **Key Features**: Clear communication, next steps
- **Tools**: None (focuses on communication)

### ℹ️ `pto_info_agent_instructions.md`
Instructions for the PTO Info Agent that answers policy questions.
- **Role**: Provide PTO policy information and calculations
- **Key Features**: Policy guidance, balance calculations
- **Tools**: Date utilities for PTO calculations

## Usage:
These instruction files are loaded by the main workflow and provide each agent with their specific role, capabilities, and communication style guidelines.

## Benefits of Separation:
- **Maintainability**: Easy to update individual agent behaviors
- **Clarity**: Clear separation of responsibilities
- **Reusability**: Instructions can be shared across deployments
- **Version Control**: Track changes to specific agent behaviors