import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ccxt
import time
import websocket
import json
import requests

st.title("EUR/USD Price")
st.write("мацаю Streamlit")
st.write("Ціни EUR/USD на 5-хвилинному таймфреймі:")

data = pd.read_csv('EURUSD_price.csv')
# st.write(data)


ohlc_data = data[['Datetime','Open', 'High', 'Low', 'Close']]

fig = go.Figure(data=[go.Candlestick(x=ohlc_data.Datetime,
                open=ohlc_data['Open'],
                high=ohlc_data['High'],
                low=ohlc_data['Low'],
                close=ohlc_data['Close'])])

fig.update_layout(
    title='EUR/USD 5-Min Candlestick Chart',
    xaxis_title='Time',
    yaxis_title='Price'
)
# sidebar
a = st.sidebar.radio('Choose:',[1,2])
st.sidebar.camera_input('camera')

st.chat_input('chat me')

# Створити стовпці для таблиці та графіка
table_col, graph_col = st.columns((1, 2))
# table_col.markdown('<style>div.css-1dbke49{width: calc(33.33% - 20px);}</style>', unsafe_allow_html=True)
# graph_col.markdown('<style>div.css-1dbke49{width: calc(66.67% - 20px);}</style>', unsafe_allow_html=True)

table_col.dataframe(ohlc_data)
graph_col.plotly_chart(fig)

# Підключення до API Binance
exchange = ccxt.binance()

# Віджет для відображення цін
st.header("Ціна біткоїна (BTC) в реальному часі")


url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# Виконати GET-запит


# Перевірити, чи запит був успішним
while True:
    response = requests.get(url)
    if response.status_code == 200:
        # Розпакувати JSON-відповідь
        data = response.json()
        # Вивести ціну біткоїна
        price = float(data["price"])
        price_widget = st.text(price)
        time.sleep(2.5)
        price_widget.empty()
    else:
        st.text("Помилка при виконанні запиту")



# Функція для обробки нових даних
# def on_message(ws, message):
#     message = json.loads(message)
#     if 'data' in message:
#         price = float(message['data']['p'])
#         price_widget.text(f"Ціна біткоїна (BTC) в USD: ${price}")
#
# # Підключення до потоку WebSocket для отримання цін біткоїна
# symbol = 'btcusdt'  # Пара торгів
# channel = f'{symbol}@ticker'  # Канал для отримання цін
# url = f"wss://stream.binance.com:9443/ws/{channel}"
#
# ws = websocket.WebSocketApp(url, on_message=on_message)

# Постійно слухати потік WebSocket
# ws.run_forever()
