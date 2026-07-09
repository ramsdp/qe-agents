# QE Agents – AI-Powered Quality Engineering Framework

## Overview

QE Agents is an AI-powered Quality Engineering framework that automates key stages of the software testing lifecycle using autonomous AI agents.

The framework demonstrates an end-to-end workflow that transforms an OpenAPI specification into executable API tests, executes those tests, and generates an AI-assisted defect report.

This project was developed as a proof-of-concept for the QE Agents Design Challenge.

---

# Features

* AI-powered Test Planning
* AI-powered Test Generation
* Automated Test Execution
* AI-assisted Defect Triaging
* Modular Agent-based Architecture
* JSON Report Generation
* End-to-End Automated Workflow

---

# Architecture

```text
                 OpenAPI Specification
                          │
                          ▼
                  Planner Agent
                          │
          Generates Risk-Based Test Plan
                          │
                          ▼
                 Generator Agent
                          │
        Generates Executable Pytest Tests
                          │
                          ▼
                  Executor Agent
                          │
         Executes Tests & Collects Results
                          │
                          ▼
                  Triager Agent
                          │
       Generates AI Defect Analysis Report
```

---

# Project Structure

```text
qe-agents/
│
├── agents/
│   ├── planner.py
│   ├── generator.py
│   ├── executor.py
│   └── triager.py
│
├── tools/
│   └── llm.py
│
├── tests/
│   └── generated/
│       └── test_pet.py
│
├── artifacts/
│   └── reports/
│       ├── test_plan.json
│       └── execution_report.json
│
├── reports/
│   └── bug_report.json
│
├── openapi/
│   └── petstore.json
│
├── main.py
├── requirements.txt
├── README.md
└── DESIGN.md
```

---

# Technology Stack

* Python
* LangGraph
* LangChain
* Google Gemini
* Pytest
* Requests
* JSON

---

# Workflow

### 1. Planner Agent

The Planner Agent reads the OpenAPI specification and creates a structured risk-based test plan.

Output:

```text
artifacts/reports/test_plan.json
```

The generated plan contains:

* Risk Assessment
* Positive Test Scenarios
* Negative Test Scenarios
* Boundary Test Scenarios

---

### 2. Generator Agent

The Generator Agent converts the generated test plan into executable pytest API test cases.

Output:

```text
tests/generated/test_pet.py
```

---

### 3. Executor Agent

The Executor Agent executes the generated test suite using pytest.

Output:

```text
artifacts/reports/execution_report.json
```

The execution report includes:

* Total Tests
* Passed Tests
* Failed Tests
* Console Output

---

### 4. Triager Agent

The Triager Agent analyses failed test cases using an LLM and generates a structured defect report.

Output:

```text
reports/bug_report.json
```

The defect report includes:

* Severity
* Priority
* Failed Tests
* Root Cause Analysis
* Recommendations

---

# Prerequisites

* Python 3.10 or later (Python 3.11 recommended)
* Google Gemini API Key

---

# Installation

Clone the repository

```bash
git clone <repository-url>
cd qe-agents
```

Create a virtual environment

```bash
python3 -m venv venv
```

Activate the virtual environment

macOS/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file in the project root.

```text
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

# Running the Project

Execute:

```bash
python main.py
```

---

# Sample Execution

```text
Planning tests...

✅ test_plan.json saved

Generating tests...

✅ Test file generated: tests/generated/test_pet.py

Executing tests...

✅ Execution report saved to artifacts/reports/execution_report.json

Triaging failures...

✅ Bug report saved: reports/bug_report.json
```

---

# Generated Artifacts

The framework automatically generates:

```text
artifacts/reports/test_plan.json

tests/generated/test_pet.py

artifacts/reports/execution_report.json

reports/bug_report.json
```

---

# Assumptions

* The supplied OpenAPI specification is valid.
* The API under test is available and reachable.
* Google Gemini API credentials are configured correctly.
* Generated tests are executed in a trusted local environment.

---

# Future Enhancements

* Parallel test execution
* Flaky test detection
* Docker sandbox for generated code
* Jira integration for automatic defect creation
* Human-in-the-loop approval workflow
* HTML reporting dashboard
* CI/CD pipeline integration
* UI automation support
* Performance testing agents
* Security testing agents
* Test coverage analytics

---

# Author

**Ramya Gunukula**

This project was developed as part of the QE Agents Design Challenge to demonstrate the application of autonomous AI agents in the Quality Engineering lifecycle.
