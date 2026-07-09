import json
import subprocess
from pathlib import Path


def executor(state):
    """
    Executes the generated pytest test file and stores the execution results.
    """

    print("\nExecuting tests...\n")

    try:
        result = subprocess.run(
            ["pytest", state["generated_test_file"], "-v"],
            capture_output=True,
            text=True
        )

        state["execution_result"] = {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

        # Create reports directory if it doesn't exist
        Path("artifacts/reports").mkdir(parents=True, exist_ok=True)

        # Save execution report
        with open("artifacts/reports/execution_report.json", "w") as f:
            json.dump(state["execution_result"], f, indent=4)

        print("✅ Execution report saved to artifacts/reports/execution_report.json")

        

    except Exception as e:
        state["execution_result"] = {
            "returncode": -1,
            "stdout": "",
            "stderr": str(e)
        }

        print(f"❌ Error while executing tests: {e}")
        

    return state