import pickle 
import pandas as pd
import matplotlib.pyplot as plt


def predict_bitcoin(df):

    # Load the model
    with open('random_forest_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    # Get the last date from the dataset
    last_date = df['Date'].max()

    # Generate the next 30 days
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, 10)]

    # future_features = pd.DataFrame({'Date': [future_date for future_date in future_dates]})
    # Transform future dates into features
    future_features = pd.DataFrame({
        'Date': [future_date for future_date in future_dates],
        'Day': [date.day for date in future_dates],
        'Month': [date.month for date in future_dates],
        'Year': [date.year for date in future_dates]
    })
    predicted_prices = loaded_model.predict(future_features[['Day', 'Month', 'Year']])
    future_features['Price'] = predicted_prices.round(2)

    # Merge historical data with future data
    combined_data = pd.concat([df,future_features ], ignore_index=True)

    # combined_data['Date'] = pd.to_datetime(df['Date'])
    # combined_data['Date'] = combined_data['Date'].apply(lambda x: x.date())
    # combined_data = combined_data.sort_values('Date')
    # # Set 'date' as the index
    # combined_data.set_index('Date', inplace=True)

    return combined_data
