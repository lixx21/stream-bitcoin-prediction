import streamlit as st
from src.connection import mongodb_connection
from src.predict_price import predict_bitcoin
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objs as go
import matplotlib.pyplot as plt

def main():
    st.set_page_config(
        page_title="Bitcoin Prediction"
    )
    # Apply custom CSS to make Streamlit container full width
    st.markdown(
        """
        <style>
        .main .block-container {
            max-width: 1600px;  /* You can set any width here */
            padding-left: 5rem;
            padding-right: 5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    #get data
    collection = mongodb_connection()
    results = collection.find({}, {"_id":0})

    data = list(results)
    df = pd.DataFrame(data)

    bitcoin_data = df.copy()

    #TODO: for prediction data
    bitcoin_data['Date'] = pd.to_datetime(bitcoin_data['Date'])
    bitcoin_data['Date'] = bitcoin_data['Date'].apply(lambda x: x.date())
    bitcoin_data = bitcoin_data.sort_values('Date')
    predicted_data = predict_bitcoin(bitcoin_data)

    #TODO: For Actual Data
    # Convert 'date' column to datetime format
    # df['Date'] = pd.to_datetime(df['Date'])
    # df['Date'] = df['Date'].apply(lambda x: x.date())
    # df = df.sort_values('Date')

    # st.title("Real Bitcoin Price")
    # real_data = go.Scatter(x=df['Date'], y=df['Price'], mode="lines", name="Price", line=dict(color='blue'))
    # layout = go.Layout(
    #     title="Bitcoin's Price"
    # )

    st.title("Forecasted Bitcoin Price")
    st.write("The forecasted data is for 10 days from now.")
    # Visualize Prediction Data

    actual_price = go.Scatter(x=bitcoin_data['Date'], y=bitcoin_data['Price'], mode='lines', name="Actual Price", line=dict(color='blue'))
    predicted_price = go.Scatter(x=predicted_data['Date'], y=predicted_data['Price'], mode='lines', name="Forcasted Price", line=dict(color='red'))
    
    data_combined = [predicted_price, actual_price]
    layout = go.Layout(
        # title= "Forcasted Bitcoin's Price",
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price'),
        height=600,
        width=1600, 
        hovermode='closest'
    )
    fig_combined = go.Figure(data=data_combined, layout=layout)
    st.plotly_chart(fig_combined, use_container_width=True)



if __name__== "__main__":
    main()

        



