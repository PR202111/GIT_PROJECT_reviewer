import os
import ast
from pathlib import Path
from git import Repo
from datetime import datetime
from CONFIG import REPO_PATH


def analyze_repo_structure(repo_path: str = REPO_PATH) -> str:
    """
    Analyze import dependencies, function definitions, and calls between files.
    Returns a single string suitable for feeding to an LLM.
    """
    repo_path = Path(repo_path)
    summary_text = f"Repository Structure Analysis for {repo_path}\n" + "=" * 80 + "\n"

    for file in repo_path.rglob("*.py"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                code = f.read()
            tree = ast.parse(code)
        except Exception as e:
            summary_text += f"\n Skipping {file.name}: {e}\n"
            continue

        imports, functions, calls = set(), [], []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)
                for n in ast.walk(node):
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
                        calls.append(n.func.id)

        summary_text += (
            f"\n{file.name}\n"
            f"├── Imports: {', '.join(sorted(imports)) or 'None'}\n"
            f"├── Functions: {', '.join(functions) or 'None'}\n"
            f"└── Calls: {', '.join(calls) or 'None'}\n"
            + "-" * 80 + "\n"
        )

    return summary_text




def get_git_history(repo_path: str = REPO_PATH, max_commits: int = 20) -> str:
    """
    Get recent git commit history for the repository.
    Returns a formatted string with author, date, message, and changed files.
    """
    try:
        repo = Repo(repo_path)
    except Exception as e:
        return f"Not a valid Git repository: {e}"

    commits = list(repo.iter_commits('HEAD', max_count=max_commits))
    if not commits:
        return "No commits found in this repository."

    history_text = f"Git History for {repo_path}\n" + "=" * 80 + "\n"

    for commit in commits:
        date = datetime.fromtimestamp(commit.committed_date).strftime("%Y-%m-%d %H:%M:%S")
        files_changed = ", ".join(commit.stats.files.keys()) or "No files listed"

        history_text += (
            f"Commit: {commit.hexsha[:8]}\n"
            f"Author: {commit.author.name} <{commit.author.email}>\n"
            f"Date: {date}\n"
            f"Message: {commit.message.strip()}\n"
            f"Files Changed: {files_changed[:600]}\n"
            + "-" * 80 + "\n"
        )

    return history_text


