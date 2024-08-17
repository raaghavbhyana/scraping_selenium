
import requests
# url = 'https://v6.exchangerate-api.com/v6/86a8424b9225e7d5fda96501/latest/USD'
try:
    url = 'https://v6.exchangerate-api.com/v6/86a8424b9225e7d5fda96501/latest/USD'

# Making our request
    response = requests.get(url)
    data = response.json()
    inr_rate = data['conversion_rates']['INR']
    print(data)
    print(inr_rate)

        
        # df["Price"] = df["Price"].str.replace(",", "").astype(float)
        # df["Final Price (INR)"] = df["Price"] * inr_rate
except Exception as e:
        print(f"Error converting to INR: {e}")
        # df["Final Price (INR)"] = None
    