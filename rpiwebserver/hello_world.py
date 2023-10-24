from flask import Flask, render_template, request
import subprocess
# this is a comment
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['GET', 'POST'])
def run_script():
    if request.method == 'POST':
        payload = request.form['payload']
        if payload == 'payload1':
            script_path = '/bunny/payloads/0/boot'
        elif payload == 'payload2':
            script_path = '/bunny/payloads/1/boot'
        elif payload == 'payload3':
            script_path = '/bunny/payloads/2/boot'
        elif payload == 'payload3':
            script_path = '/bunny/payloads/2/boot'
        elif payload == 'payload18':
            script_path = '/bunny/payloads/2/boot'
        else:
            return 'Invalid payload'
        subprocess.run(['bash', script_path])
        return 'Script executed successfully!'
    else:
        return 'Invalid request method'


if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
