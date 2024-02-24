from flask import Flask, request, jsonify
from pypsrp.client import Client
import psycopg2
from psycopg2.extras import RealDictCursor


app = Flask(__name__)

def get_mssql_credentials(data):
    return (
        data.get('mssql_host'),
        data.get('mssql_port'),
        data.get('mssql_username'),
        data.get('mssql_password'),
        data.get('mssql_database')
    )

def execute_mssql_query(host, port, username, password, database, query):
    try:
        with Client(host, username=username, password=password, port=port, ssl=False) as pypsrp_client:
            script = f"$result = Measure-Command {{ Invoke-Sqlcmd -ServerInstance '{host}' -Database '{database}' -Username '{username}' -Password '{password}' -Query '{query}' }}; $result.TotalMilliseconds"
            result = pypsrp_client.execute_ps(script)

        latency = float(result[0].strip())
        return latency

    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def get_psql_credentials(data):
    return (
        data.get('psql_host'),
        data.get('psql_port'),
        data.get('psql_username'),
        data.get('psql_password'),
        data.get('psql_database')
    )

def execute_psql_query(host, port, username, password, database, query):
    try:
        with psycopg2.connect(host=host, port=port, user=username, password=password, database=database) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        return result

    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
def execute_psql_query_latency(host, port, username, password, database, query):
    try:
        with psycopg2.connect(host=host, port=port, user=username, password=password, database=database) as conn:
            with conn.cursor() as cursor:
                script = f"EXPLAIN ANALYZE {query}"
                cursor.execute(script)
                result = cursor.fetchone()

        # Extracting the execution time from the result
        execution_plan = result[0]
        start_index = execution_plan.find('Total runtime:')
        end_index = execution_plan.find('ms', start_index)
        latency = float(execution_plan[start_index + len('Total runtime:'):end_index].strip())

        return latency

    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}


@app.route('/automation/api/1.0/psql/execute_query', methods=['POST'])
def execute_psql_query_endpoint():
    try:
        data = request.get_json()
        psql_credentials = get_psql_credentials(data)
        sql_query = data.get('sql_query')

        result = execute_psql_query(*psql_credentials, sql_query)

        return jsonify({'Status': 'Success', 'Result': result})
    except Exception as e:
        return jsonify({'Status': 'Failure', 'Message': f"An error occurred: {str(e)}"}), 500


@app.route('/automation/api/1.0/mssql/check_query_latency', methods=['POST'])
def check_query_latency():
    try:
        data = request.get_json()
        mssql_credentials = get_mssql_credentials(data)
        sql_query = data.get('sql_query')

        latency = execute_mssql_query(*mssql_credentials, sql_query)

        return jsonify({'Status': 'Success', 'Latency(ms)': latency})
    except Exception as e:
        return jsonify({'Status': 'Failure', 'Message': f"An error occurred: {str(e)}"}), 500


@app.route('/automation/api/1.0/psql/check_query_latency', methods=['POST'])
def check_psql_query_latency():
    try:
        data = request.get_json()
        psql_credentials = get_psql_credentials(data)
        sql_query = data.get('sql_query')

        latency = execute_psql_query_latency(*psql_credentials, sql_query)

        return jsonify({'Status': 'Success', 'Latency(ms)': latency})
    except Exception as e:
        return jsonify({'Status': 'Failure', 'Message': f"An error occurred: {str(e)}"}), 500

@app.route('/automation/api/1.0/mssql/execute_query', methods=['POST'])
def execute_mssql_query_endpoint():
    try:
        data = request.get_json()
        mssql_credentials = get_mssql_credentials(data)
        sql_query = data.get('sql_query')

        result = execute_mssql_query(*mssql_credentials, sql_query)

        return jsonify({'Status': 'Success', 'Result': result})
    except Exception as e:
        return jsonify({'Status': 'Failure', 'Message': f"An error occurred: {str(e)}"}), 500






# Install necessary packages:
# pip install flask psycopg2

# Replace these with your PostgreSQL database credentials
DB_HOST = 'loca lhost'
DB_PORT = 5432
DB_NAME = 'new'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

# API endpoint to check latency
@app.route('/api/latency', methods=['GET'])
def check_latency():
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        # Open a cursor to perform database operations
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Execute a simple query to measure latency
        cursor.execute("SELECT 1")

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Return the latency in the response
        return jsonify({'latency': 'Database is reachable', 'data': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
