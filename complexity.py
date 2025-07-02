from radon.complexity import cc_visit

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
