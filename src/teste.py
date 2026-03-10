import pandas as pd

def parse_datetime(v):
    if pd.isna(v):
        return None
    try:
        dt = pd.to_datetime(v)          
        dt = dt + pd.Timedelta(hours=3) 
        return dt.isoformat()
    except:
        return None

print(parse_datetime("2026-03-09T19:00:00+00:00"))