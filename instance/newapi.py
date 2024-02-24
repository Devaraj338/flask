from flask import Flask, request, jsonify
import psycopg2
import subprocess
import shlex  # For safe shell command splitting

app = Flask(__name__)

# Replace these with your actual PostgreSQL and PowerShell configurations
POSTGRESQL_CONFIG = {
    'host': 'localhost',
    'database': 'dev',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432',
}

POWERSHELL_CONFIG = {
    'host': 'local host',
    'username': 'DevaMuralee',
    'password': '2580',
    'port': '5985',
}

def execute_postgresql_query(query):
    try:
        connection = psycopg2.connect(**POSTGRESQL_CONFIG)
        cursor = connection.cursor()

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result

    except Exception as e:
        return str(e)

def execute_powershell_command(command):
    try:
        # Construct the PowerShell command
        powershell_command = f'powershell.exe {command}'
        
        # Execute the PowerShell command using subprocess
        result = subprocess.run(shlex.split(powershell_command), capture_output=True, text=True)

        # Check if there were any errors
        result.check_returncode()

        return result.stdout

    except subprocess.CalledProcessError as e:
        return f"Error executing PowerShell command: {e.stderr}"

@app.route('/api/execute_query', methods=['POST'])
def execute_query():
    try:
        data = request.get_json()
        query = data.get('query')
        windows_credentials = data.get('windows_credentials')

        if not query or not windows_credentials:
            return jsonify({'Status': 'Failure', 'Message': 'Invalid or missing query or Windows credentials'}), 400

        # Execute PostgreSQL query
        postgresql_result = execute_postgresql_query(query)

        # Execute PowerShell command
        powershell_command = f'Write-Host "PostgreSQL Result: {postgresql_result}"'
        powershell_result = execute_powershell_command(powershell_command)

        return jsonify({'Status': 'Success', 'PostgreSQL_Result': postgresql_result, 'PowerShell_Result': powershell_result})

    except Exception as e:
        return jsonify({'Status': 'Failure', 'Message': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
