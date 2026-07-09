import json
from pathlib import Path

from tools.llm import get_llm


def planner(state):
    """
    Creates a test plan from an API specification using LLM.
    """

    print("\nPlanning tests...\n")

    llm = get_llm()

    prompt = f"""
You are a Senior QA Engineer.

Read the following API specification.

{state["spec"]}

Return ONLY valid JSON in this format:

{{
  "risk": "High",
  "positive": [...],
  "negative": [...],
  "boundary": [...]
}}
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    # Remove markdown if LLM returns JSON inside code block
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        # Convert JSON string to Python dictionary
        state["test_plan"] = json.loads(content)

    except json.JSONDecodeError:
        print("❌ LLM returned invalid JSON:")
        print(content)
        raise

    # Create reports folder
    Path("artifacts/reports").mkdir(
        parents=True,
        exist_ok=True
    )

    # Save test plan JSON
    with open("artifacts/reports/test_plan.json", "w") as f:
        json.dump(
            state["test_plan"],
            f,
            indent=4
        )

    print("✅ test_plan.json saved")

    return state
