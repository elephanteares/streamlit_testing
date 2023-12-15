from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def get_actual_intensity(date):
    url = f'https://api.carbonintensity.org.uk/intensity/date/{date}'
    r = requests.get(url)
    
    if r.status_code == 200:
        data = r.json()
        actual_intensity = data['data'][0]['intensity']['actual']
        return actual_intensity
    else:
        return None

@app.route('/')
def home():
    default_date = '01-01-2022'
    date = request.args.get('date', default_date)
    actual_intensity = get_actual_intensity(date)
    return render_template('form.html', date=date, actual_intensity=actual_intensity)

@app.route('/form', methods=['POST', 'GET'])
def form():
    date = None
    actual_intensity = None

    if request.method == 'POST':
        date = request.form.get('date')
        actual_intensity = get_actual_intensity(date)
        return render_template('submitted.html', date=date, actual_intensity=actual_intensity)

    return render_template('form.html', date=date, actual_intensity=actual_intensity)

if __name__ == '__main__':
    app.run(debug=True)