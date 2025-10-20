TOOLS =  [
    {
        "name": "AnalyzeCodeQuality",
        "func": "analyze_code_quality",
        "module": "static_tools",
        "description": "Analyze a code string for style and maintainability issues."
    },
    {
        "name": "AnalyzeDocstrings",
        "func": "analyze_docstrings",
        "module": "static_tools",
        "description": "Check which functions lack docstrings."
    },
    {
        "name": "AnalyzeComplexity",
        "func": "analyze_complexity",
        "module": "static_tools",
        "description": "Compute cyclomatic complexity metrics for code."
    },
    {
        "name": "AnalyzeRepoStructure",
        "func": "analyze_repo_structure",
        "module": "analysize_repo",
        "description": "Inspect imports, functions, and calls in a repo."
    },
    {
        "name": "GetGitHistory",
        "func": "get_git_history",
        "module": "analysize_repo",
        "description": "Summarize recent git commits, authors, and changes."
    },
    {
        "name": "QueryVectorStore",
        "func": "query_vector_store",
        "module": "documents_to_database",
        "description": "Search the code repository using the vector store.",
        "dependencies": ["vector_store"]  
    }
]
