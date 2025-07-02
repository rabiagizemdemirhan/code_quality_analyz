import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def plot_folder_complexity_interactive(complexity_results):
    all_data = []
    for file_name, functions in complexity_results.items():
        for func in functions:
            all_data.append({
                "File": file_name,
                "Function": func["name"],
                "Complexity": func["complexity"]
            })

    df = pd.DataFrame(all_data)

    fig = px.bar(df, x="Function", y="Complexity", color="Complexity",
                 hover_data=["File"], barmode="group",
                 color_continuous_scale=["#7FFF00", "#FFD700", "#FF0000"],
                 title="Function-Level Complexity Scores (All Files)")

    return fig

def plot_metrics_interactive(data):
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="file",
        y="avg_function_length",
        color="max_function_length",
        hover_data=["line_count", "function_count", "max_function_length"],
        title="Function Lengths per File",
        labels={
            "file": "File Name",
            "avg_function_length": "Avg. Function Length",
            "max_function_length": "Max Function Length"
        }
    )

    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_metrics(data):
    files = [item['file'] for item in data]
    funcs = [item['function_count'] for item in data]
    avg_len = [item['avg_function_length'] for item in data]

    plt.figure(figsize=(10, 5))
    plt.bar(files, funcs, label="Function Count")
    plt.bar(files, avg_len, label="Avg. Function Length", bottom=funcs)
    plt.title("Function Count and Length")
    plt.xlabel("File")
    plt.ylabel("Metrics")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/metric_graph.png")

def plot_complexity_bar(complexity_data):
    names = [block['name'] for block in complexity_data]
    complexities = [block['complexity'] for block in complexity_data]
    ranks = [block['rank'] for block in complexity_data]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(names, complexities, color="skyblue")

    plt.xlabel("Function Name")
    plt.ylabel("Complexity")
    plt.title("Cyclomatic Complexity (Radon CC)")
    plt.xticks(rotation=45)

    for bar, rank in zip(bars, ranks):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), rank,
                 ha='center', va='bottom', fontsize=8, color='gray')

    plt.tight_layout()
    plt.savefig("output/complexity_graph.png")
