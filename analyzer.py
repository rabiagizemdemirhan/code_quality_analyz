import os
import ast
from radon.complexity import cc_visit

def analyze_python_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    tree = ast.parse(content)
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

    function_lengths = []
    for func in functions:
        start = func.lineno
        if hasattr(func, 'end_lineno'):
            end = func.end_lineno
        else:
            end = max([node.lineno for node in ast.walk(func) if hasattr(node, 'lineno')], default=start)
        function_lengths.append(end - start + 1)

    return {
        "file": os.path.basename(file_path),
        "line_count": len(content.splitlines()),
        "function_count": len(functions),
        "avg_function_length": round(sum(function_lengths) / len(function_lengths), 2) if functions else 0,
        "max_function_length": max(function_lengths, default=0) if function_lengths else 0
    }

def analyze_folder(folder_path):
    result = []
    for file in os.listdir(folder_path):
        if file.endswith(".py"):
            full_path = os.path.join(folder_path, file)
            if os.path.isfile(full_path):
                result.append(analyze_python_file(full_path))
    return result

def get_radon_complexity(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        complexity_data = cc_visit(code)
        return [
            {
                "name": getattr(item, 'name', 'Unknown'),
                "complexity": getattr(item, 'complexity', 0),
                "lineno": getattr(item, 'lineno', 0),
                "rank": getattr(item, 'rank', 'N/A')
            }
            for item in complexity_data
        ]
    except Exception as e:
        print(f"Error reading or analyzing {file_path}: {e}")
        return []

if __name__ == "__main__":
    from pprint import pprint

    analysis = analyze_folder("target_code")
    pprint(analysis)
