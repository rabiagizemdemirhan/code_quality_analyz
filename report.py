import pandas as pd

def export_to_csv(data, path="output/analysis_report.csv"):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
