import pandas as pd


def load_and_sort_csv(file_path):
    df = pd.read_csv(file_path)
    df['createdDate'] = pd.to_datetime(df['createdDate'])
    sorted_df = df.sort_values(by='createdDate', ascending=False)

    return sorted_df


file_path = 'output1.csv'
sorted_df = load_and_sort_csv(file_path)

sorted_df.to_csv(file_path, index=False)
