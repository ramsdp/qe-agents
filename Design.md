QE Agents – Design Document
Objective
The objective of this project is to demonstrate how autonomous AI agents can improve the Quality
Engineering lifecycle by automating repetitive tasks while still applying engineering reasoning.
The system focuses on delivering an end-to-end workflow:
OpenAPI Specification
↓
Risk-Based Test Planning
↓
Executable Test Generation
↓
Automated Test Execution
↓
AI Defect Triaging
Rather than building a production platform, the objective was to demonstrate a complete working slice
that showcases agent collaboration.
Architecture
The solution follows an agent-based architecture.
Each agent performs one well-defined responsibility and communicates using a shared workflow state.
OpenAPI Specification
│
▼
Planner Agent
│
▼
Generator Agent
│
▼
Executor Agent
│
▼
Triager Agent
Each agent receives the current workflow state, performs its task, updates the state, and passes it to the
next agent.
This design makes the system modular and allows individual agents to evolve independently.
Agent Responsibilities
Planner Agent
Responsibilities
Parse API specification
Understand endpoints
Identify business risks
Generate risk-based scenarios
Produce positive tests
Produce negative tests
Produce boundary tests
Output
test_plan.json
Generator Agent
Responsibilities
Read the generated test plan
Generate executable pytest API tests
Produce maintainable Python code
Organize tests by scenario
Output
tests/generated/test_pet.py

Executor Agent
Responsibilities
Execute generated tests
Capture console logs
Record pass/fail statistics
Generate execution reports
Output
execution_report.json
Triager Agent
Responsibilities
Analyse execution failures
Identify likely root cause
Estimate severity
Estimate priority
Recommend corrective actions
Output
bug_report.json
State Management
The workflow shares information through a common state object.
Example
state = {
"spec": "...",
"test_plan": {...},
"generated_tests": "...",
"execution_result": "...",

"bug_report": "..."
}
This avoids unnecessary coupling between agents.
Framework Selection
LangGraph
LangGraph was selected because it naturally represents agent workflows as graphs.
Benefits
Simple orchestration
Shared state
Easy future branching
Human-in-the-loop support
Retry support
Scalable architecture
Google Gemini
Gemini was selected because it provides:
Strong reasoning capabilities
Good code generation
Large context window
Fast responses
Easy Python integration
The model performs well for:
Test planning
Test generation
Failure analysis
Design Decisions
The project deliberately separates planning, generation, execution and triaging.
Benefits include:
Single responsibility
Easier maintenance

Better testing
Replaceable agents
Independent improvements
Trade-offs
Several design decisions were made to balance simplicity and functionality.
Advantages
Modular architecture
Easy to extend
Clear workflow
Reusable agents
Simple CLI execution
Limitations
Sequential execution
No parallel test execution
No flaky-test detection
No Jira integration
No Docker sandbox
No human approval workflow
Supports API testing only
These were considered acceptable for a proof-of-concept.
Evaluation
The system was evaluated using the Swagger Petstore API.
The workflow successfully:
Generated a structured risk-based test plan
Produced executable pytest API tests
Executed the generated tests
Detected failures
Generated an AI-assisted defect report
The resulting defect report included:
Severity
Priority
Root Cause
Failed Tests
Recommendations

This demonstrates that the end-to-end workflow functions correctly.
Future Improvements
Future work would focus on production readiness.
Test Planning
Requirement ambiguity detection
Requirement traceability
Coverage metrics
Test Generation
UI automation
Performance testing
Security testing
Contract testing
Execution
Parallel execution
Docker sandbox
Kubernetes execution
Retry logic
Flaky test identification
Defect Management
Jira integration
Duplicate defect detection
AI owner recommendation
Historical defect clustering
Reporting
HTML dashboard
Trend analysis
Test coverage reports
CI/CD integration
Conclusion
The solution demonstrates how AI agents can automate key stages of the Quality Engineering lifecycle
while remaining modular, extensible and maintainable.

