import streamlit as st
import os
import shutil
from analyzer import analyze_folder, get_radon_complexity
from report import export_to_csv
from visualize import plot_metrics, plot_complexity_bar, plot_metrics_interactive
from pdf_report import create_pdf_report

def _get_radon_rank_description(rank):
    descriptions = {
        'A': "Very low risk – easy to maintain",
        'B': "Low risk – readable",
        'C': "Moderate risk – caution advised",
        'D': "High risk – should be simplified",
        'E': "Very high risk – hard to maintain",
        'F': "Rewrite recommended"
    }
    return descriptions.get(rank, "Unknown")

# Prepare temporary and output folders
if os.path.exists("temp_uploaded_files"):
    shutil.rmtree("temp_uploaded_files")
os.makedirs("temp_uploaded_files", exist_ok=True)

os.makedirs("output", exist_ok=True)

# Streamlit layout setup
st.set_page_config(layout="wide")
st.title("📂 Python Code Quality Analyzer")

# Section 1: Folder Analysis
st.header("1. Folder Analysis")
folder = st.text_input("Enter folder path to analyze:", "target_code", help="Enter the root folder of your project or the folder you want to analyze (e.g., target_code)")

if st.button("Analyze Folder"):
    if not os.path.isdir(folder):
        st.error(f"The folder '{folder}' does not exist or is not valid. Please enter a correct path.")
    else:
        with st.spinner("Analyzing folder... This may take a moment."):
            result = analyze_folder(folder)
        if result:
            st.success("Folder analysis completed!")

            # ✅ Generate PDF report
            create_pdf_report(result)
            pdf_path = "output/code_analysis_report.pdf"
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=f.read(),
                        file_name="code_analysis_report.pdf",
                        mime="application/pdf"
                    )

            st.subheader("📊 Overall Analysis Results")
            st.write(result)

            st.subheader("📊 Interactive Metrics Chart")
            st.plotly_chart(plot_metrics_interactive(result))

            export_to_csv(result)
            plot_metrics(result)

            st.subheader("Charts and Reports")
            st.image("output/metric_graph.png", caption="Code Quality Metrics Graph")
            st.download_button(
                label="📥 Download Analysis Report (CSV)",
                data=open("output/analysis_report.csv", "rb").read(),
                file_name="analysis_report.csv",
                mime="text/csv"
            )

            st.subheader("📄 Detailed Function List and Complexity Evaluation")
            complexity_results = {}

            for file in os.listdir(folder):
                if file.endswith(".py"):
                    full_path = os.path.join(folder, file)
                    if os.path.isfile(full_path):
                        complexity_data_for_file = get_radon_complexity(full_path)
                        if complexity_data_for_file:
                            complexity_results[file] = complexity_data_for_file

            if complexity_results:
                for file_name, functions_data in complexity_results.items():
                    st.markdown(f"### 📘 {file_name}")
                    for func in functions_data:
                        rank_desc = _get_radon_rank_description(func['rank'])
                        emoji = "✅"
                        if func['rank'] in ['D', 'E']:
                            emoji = "⚠️"
                        elif func['rank'] == 'F':
                            emoji = "❌"
                        st.markdown(
                            f"- {emoji} `{func['name']}` (line {func['lineno']}) → **Complexity:** {func['complexity']} → **Rank:** {func['rank']} ({rank_desc})"
                        )
            else:
                st.info(f"No analyzable functions or classes found in the Python files inside '{folder}'.")
        else:
            st.warning(f"No Python files found in '{folder}'. Please make sure the folder contains .py files.")

# Section 2: Single File Radon Complexity Analysis
st.header("2. Single File Complexity (Radon) Analysis")
st.info("This section shows the functional complexity of the selected Python file. High complexity may make code harder to understand and maintain.")

uploaded_file = st.file_uploader("Please select a Python file (.py):", type=["py"])

if uploaded_file is not None:
    temp_file_path = os.path.join("temp_uploaded_files", uploaded_file.name)

    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.subheader(f"📄 Complexity Analysis for '{uploaded_file.name}'")
    try:
        complexity_data = get_radon_complexity(temp_file_path)
        if complexity_data:
            for block in complexity_data:
                st.write(
                    f"➡️ `{block['name']}` (line {block['lineno']}): "
                    f"complexity = `{block['complexity']}` → **Rank:** `{block['rank']}` "
                    f"({_get_radon_rank_description(block['rank'])})"
                )

            plot_complexity_bar(complexity_data)
            st.image("output/complexity_graph.png", caption="Functional Complexity Graph")

        else:
            st.warning(f"No functions or classes to analyze in '{uploaded_file.name}'. Please ensure the file contains valid Python code.")

    except Exception as e:
        st.error(f"An error occurred during Radon analysis: **{e}**. Please make sure your uploaded file is a valid Python file with correct syntax.")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
