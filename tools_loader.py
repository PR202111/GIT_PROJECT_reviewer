import importlib
from functools import partial
import inspect
from pydantic import create_model
from pydantic.fields import PydanticUndefined
from pathlib import Path
from langchain_core.tools.structured import StructuredTool
from documents_to_database import create_vector_store_from_repo
from CONFIG import REPO_PATH
from tools_registry import TOOLS



def make_structured_tool(name, func, description, exclude_args=None):
    """
    Convert a Python function to a StructuredTool with dynamic args.
    `exclude_args` is a list of argument names to remove from schema (e.g., injected dependencies)
    """
    sig = inspect.signature(func)
    fields = {}
    for param in sig.parameters.values():
        ann = param.annotation if param.annotation != inspect.Parameter.empty else str
        default = param.default if param.default != inspect.Parameter.empty else PydanticUndefined
        fields[param.name] = (ann, default)

    ArgsModel = create_model(f"{name}Args", **fields)

    # Remove any excluded args from schema
    if exclude_args:
        for arg in exclude_args:
            if arg in ArgsModel.model_fields:
                del ArgsModel.model_fields[arg]

    return StructuredTool.from_function(
        func=func,
        name=name,
        description=description,
        args_schema=ArgsModel
    )



def load_tools(tool_registry, **dependencies):
    """Load tools and inject dependencies without messing up defaults."""
    tools = []
    for tool_def in tool_registry:
        module = importlib.import_module(tool_def["module"])
        func = getattr(module, tool_def["func"])

        exclude_args = tool_def.get("dependencies", [])


        tool = make_structured_tool(tool_def["name"], func, tool_def["description"], exclude_args=exclude_args)


        if exclude_args:
            dep_args = [dependencies[d] for d in exclude_args]
            tool.func = partial(tool.func, *dep_args)

        tools.append(tool)
    return tools



def create_tool_list(repo_path=REPO_PATH):
    print("📚 Creating or loading vector store...")
    vector_store = create_vector_store_from_repo(REPO_PATH)



    print("🧩 Loading tools...")
    tools = load_tools(TOOLS, vector_store=vector_store)

    print("\n✅ Tools loaded:\n")
    for tool in tools:
        print(f"Tool name: {tool.name}")
        print(f"Description: {tool.description}")
        print("Arguments schema:")
        for arg_name, field in tool.args_schema.model_fields.items():
            default = field.default if field.default is not PydanticUndefined else 'Required'
            print(f"  - {arg_name}: {field.annotation}, default={default}")
        print("-" * 50)
    return tools
