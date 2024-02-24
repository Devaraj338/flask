from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get_services', methods=['GET'])
def get_services():
    try:
        # PowerShell command to get services
        pscmd = "Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias (Get-NetAdapter | Where-Object {$_.Status -eq 'Up' -and $_.Name -notlike '*Loopback*'}).InterfaceAlias).IPAddress"

        # Execute PowerShell command using subprocess
        import subprocess
        result = subprocess.run(["powershell", "-Command", pscmd], capture_output=True, text=True)

        # Check if the PowerShell command executed successfully
        if result.returncode == 0:
            # Extract output from the PowerShell command
            script_output = result.stdout.strip().splitlines()
            return jsonify({'services': script_output})
        else:
            return jsonify({'error': 'Failed to execute PowerShell command'})

    except Exception as e:
        return jsonify({'error': f'Error occurred: {e}'})

if __name__ == '__main__':
    app.run(debug=True)
