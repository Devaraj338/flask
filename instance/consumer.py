from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

def uninstall_software(hostname, username, password, package_name):
    try:
        # SSH connection setup
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname, username=username, password=password)

        # Command to uninstall software
        command = f"sudo apt-get remove {package_name} -y"  # Adjust for other package managers if needed

        # Execute the command
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode('utf-8')

        ssh_client.close()
        return output
    except paramiko.AuthenticationException:
        return "Authentication failed. Check credentials."
    except paramiko.SSHException as e:
        return f"SSH error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/uninstall_software', methods=['POST'])
def handle_uninstall_request():
    data = request.get_json()
    hostname = data.get('hostname')
    username = data.get('username')
    password = data.get('password')
    package_name = data.get('package_name')

    if not all([hostname, username, password, package_name]):
        return jsonify({'error': 'Missing required parameters.'}), 400

    result = uninstall_software(hostname, username, password, package_name)
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
