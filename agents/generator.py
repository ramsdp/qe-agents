from pathlib import Path

from tools.llm import get_llm


def generator(state):
    """
    Generates pytest API test cases from the test plan using the LLM.
    """

    print("\nGenerating tests...\n")

    llm = get_llm()

    prompt = f"""
You are a Senior QA Automation Engineer.

Generate executable pytest API tests based on the following test plan.

Test Plan:
{state["test_plan"]}

Requirements:
- Use pytest
- Use requests library
- Use https://petstore.swagger.io/v2 as the base URL
- Generate multiple positive, negative and boundary test cases
- Include meaningful test names
- Include assertions
- Return ONLY valid Python code
- Do NOT include markdown code fences
"""

    response = llm.invoke(prompt)

    code = response.content.strip()

    # Remove markdown code fences if present
    if code.startswith("```"):
        code = code.replace("```python", "")
        code = code.replace("```", "")
        code = code.strip()

    # Create directory if it doesn't exist
    Path("tests/generated").mkdir(parents=True, exist_ok=True)

    filename = "tests/generated/test_pet.py"

    # Save generated test file
    with open(filename, "w") as f:
        f.write(code)

    state["generated_test_file"] = filename

    print(f"✅ Test file generated: {filename}")

    return state