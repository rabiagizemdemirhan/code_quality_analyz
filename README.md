# 📊 Python Code Quality Analyzer

**Python Code Quality Analyzer** is an interactive web app built with Streamlit that helps developers analyze the quality and complexity of their Python codebase using static analysis techniques, visualizations, and detailed reports.

---

## 🚀 Features

- 📂 Analyze all `.py` files in a selected folder
- 📊 Collect file-level and function-level metrics
- 🧠 Evaluate cyclomatic complexity using Radon
- 📈 Visualize code metrics with Plotly & Matplotlib
- 📄 Export results as downloadable **PDF** and **CSV**
- 📥 Upload a single `.py` file for isolated complexity analysis

---

## 📐 Metrics Collected

- File name
- Total line count
- Function count
- Average function length
- Longest function
- Cyclomatic complexity scores and ranks (A–F)

---

## ⚙️ Technologies Used

- `Python`
- `Streamlit`
- `Radon`
- `Plotly`
- `Matplotlib`
- `FPDF`
- `Pandas`

---

## 📁 Project Structure

code_quality_analyzer/
│
├── analyzer.py            # Static code analysis logic
├── app.py                 # Streamlit application interface
├── pdf_report.py          # PDF generation module
├── report.py              # CSV export module
├── visualize.py           # All graphing and plots
├── requirements.txt       # Project dependencies
├── target_code/           # Folder with sample code for analysis
├── output/                # All exported files (PDF, CSV, PNG)
└── README.md              # Project documentation


---

## ▶️ Getting Started

### 1. Clone the Repository

```bash
git clone [https://github.com/yourusername/code_quality_analyzer.git](https://github.com/yourusername/code_quality_analyzer.git)
cd code_quality_analyzer
2. Set Up a Virtual Environment (Optional)
Bash

python3 -m venv venv
source venv/bin/activate       # macOS/Linux
# Or
venv\Scripts\activate          # Windows
3. Install Dependencies
Bash

pip install -r requirements.txt
4. Run the App
Bash

streamlit run app.py
Open http://localhost:8501 in your browser.

🖼️ Output Examples
📄 code_analysis_report.pdf → Full code quality summary

📥 analysis_report.csv → All file/function metrics

📊 metric_graph.png → Function count & avg length chart

📉 complexity_graph.png → Cyclomatic complexity chart

🧠 Cyclomatic Complexity Rankings (Radon)
Rank

Meaning

A

Very low risk – easy to maintain

B

Low risk – readable

C

Moderate risk – caution advised

D

High risk – refactor recommended

E

Very high risk – hard to test

F

Critical – consider rewriting


E-Tablolar'a aktar
🤝 Contributing
Pull requests, ideas, and issues are welcome!
Let's improve the Python code quality ecosystem together.

📝 License
This project is licensed under the MIT License.

👩‍💻 Developed by
Rabia Gizem Demirhan
www.linkedin.com/in/rabia-gizem-demirhan-39863a209