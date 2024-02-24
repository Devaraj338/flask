from flask import Flask, jsonify
from pypsrp.client import Client
from pypsrp.exceptions import WinRMOperationTimeoutError, PowerShellException

app = Flask(__name__)

hostname = "DevaMuralee"
port = 5985
username = ""
password = ""

@app.route('/')
def index():
    return "Flask app running!"

@app.route('/current_directory')
def get_current_directory():
    with Client(hostname, username=username, password=password, port=port, ssl=False) as client:
        try:
            pscmd = "Get-Location"
            script_result = client.execute_ps(pscmd)
            script_output = script_result[0].strip()
            return jsonify({'current_directory': script_output})
        except (WinRMOperationTimeoutError, PowerShellException) as e:
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()
