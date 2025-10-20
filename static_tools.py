# static_tools.py
import ast
import radon.complexity as complexity
import re

def analyze_code_quality(code: str) -> str:
    issues = []
    if "import *" in code:
        issues.append("Avoid using wildcard imports ('import *').")
    if "print(" in code:
        issues.append("Consider replacing 'print' with logging for production code.")
    if len(code.splitlines()) > 300:
        issues.append("File seems long — consider splitting into smaller modules.")
    return "\n".join(issues) if issues else "No major style issues found."

def analyze_complexity(code: str) -> str:
    try:
        results = complexity.cc_visit(code)
        report = [
            f"{func.name} - Complexity: {func.complexity}"
            for func in results
        ]
        return "\n".join(report) or "No functions detected."
    except Exception as e:
        return f"Error analyzing complexity: {e}"

def analyze_docstrings(code: str) -> str:
    try:
        tree = ast.parse(code)
        missing = [
            node.name for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and ast.get_docstring(node) is None
        ]
        return "Functions missing docstrings:\n" + "\n".join(missing) if missing else "All functions documented."
    except Exception as e:
        return f"Error analyzing docstrings: {e}"
