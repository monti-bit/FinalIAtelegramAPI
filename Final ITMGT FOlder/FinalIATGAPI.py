from flask import Flask, render_template, request, redirect, url_for
import requests
from pymongo import MongoClient

app = Flask(__name__)

TELEGRAM_TOKEN = "8783020004:AAGrJAqlPAirLg_f7VEbhmFqLY9msMVJ5hQ"
CHAT_ID = "7386548143"
MONGO_URI = "mongodb://localhost:27017/" 

client = MongoClient(MONGO_URI)
db = client['shaving_bar_biz'] 
orders = db['incoming_orders'] 

@app.route('/')
def home():
    return render_template('FinalIAHTML.html')

@app.route('/submit-order', methods=['POST'])
def submit_order():
    customer = request.form.get('customer')
    service = request.form.get('service')
    refno = request.form.get('refno')
    time = request.form.get('time')

    order_data = {
        "customer": customer,
        "service": service,
        "payment ref": refno,
        "appointment_time": time,
        "status": "New"
    }
    result = orders.insert_one(order_data)
    
    send_telegram(customer, service, refno, time, result.inserted_id)
    
    return f"Order for {customer} saved! Check your Telegram."

def send_telegram(customer, service, refno, time, mongo_id):
    message = (
        f"📦 *NEW ORDER RECEIVED*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"**Customer:** {customer}\n"
        f"**Service:** {service}\n"
        f"**Ref:** {refno}\n"
        f"**Time:** {time}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🆔 _ID: {mongo_id}_"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)