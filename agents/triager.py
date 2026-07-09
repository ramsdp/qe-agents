from tools.llm import get_llm
import json
from pathlib import Path


def triager(state):
    """
    Analyzes pytest execution failures using LLM
    and generates an AI-based bug report.
    """

    print("\nTriaging failures...\n")

    llm = get_llm()

    execution_result = state.get("execution_result", "")

    if not execution_result:
        state["bug_report"] = "No execution results available for analysis."
        return state

    prompt = f"""
You are a Senior QA Automation Engineer.

Analyze the following pytest execution output.

Pytest Execution Result:
-------------------------
{execution_result}
-------------------------

Generate a structured defect report.

Return the response in this format:

Severity:
(Critical / High / Medium / Low)

Priority:
(P0 / P1 / P2 / P3)

Failed Test:
(Test name if available)

Root Cause:
(Explain the probable technical reason)

Recommendation:
(Suggest the fix or next investigation steps)
"""

    response = llm.invoke(prompt)

    bug_report = response.content

    # Save in workflow state
    state["bug_report"] = bug_report

    # Create reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # Save JSON bug report
    bug_report_file = reports_dir / "bug_report.json"

    with open(bug_report_file, "w") as file:
        json.dump(
            {
                "bug_report": bug_report,
                "execution_result": execution_result
            },
            file,
            indent=4
        )

    print("\nGenerated Bug Report:\n")
    print(bug_report)

    print(f"\nBug report saved: {bug_report_file}")

    return state