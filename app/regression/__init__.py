import pandas as pd

def analyze():
    data = [['tom', 10], ['nick', 15], ['juli', 14]] 
    df = pd.DataFrame(data, columns = ['Name', 'Age']) 
    df 
    return df.to_json()