import pandas as pd

FILE_PATH = "data/Houses_in_Nigera.csv"


def load_data():
    return pd.read_csv(FILE_PATH)

def save_data(df):
    df.to_csv(FILE_PATH, index=False)

def get_houses_by_state(state):
    df = load_data()
    return df[df["state"].str.lower() == state.lower()]

def get_affordable_houses(state, min_price=200000, max_price=450000):
    df = get_houses_by_state(state)

    return df[df
        (df["monthly_price"] >= min_price) &
        (df["monthly_price"] <= max_price)
    ]

def get_house_by_id(house_id):
    df = load_data()
    return df.iloc[house_id]
    
def update_house(house_id, **updates):
    df = load_data()

    for key, value in updates.items():
        df.at[house_id, key] = value

    save_data(df)
    return df.iloc[house_id]


