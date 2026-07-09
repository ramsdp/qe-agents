from typing import TypedDict


class QEState(TypedDict):
    spec: str
    test_plan: dict
    generated_test_file: str
    execution_result: dict
    bug_report: dict