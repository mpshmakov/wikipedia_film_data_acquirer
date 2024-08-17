import pandas as pd

def exportToCsv(df: pd.DataFrame):
    df.to_csv("../exported.csv")

def exportToJson(df: pd.DataFrame):
    df.to_json("../exported.json", default_handler=str)
