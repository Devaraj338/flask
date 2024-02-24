import paramiko
from openpyxl import Workbook

def gather_server_health(ip_address, username, password):
    try:
        # SSH Connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip_address, username=username, password=password)

        # Commands to gather server health
        commands = [
            "uptime",
            "free -m",
            "df -h"
            # Add more commands as needed for health check
        ]

        # Execute commands and gather output
        health_data = {}
        for command in commands:
            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read().decode('utf-8')
            health_data[command] = output

        ssh_client.close()
        return health_data
    except Exception as e:
        return f"Error: {str(e)}"


# List of servers with their credentials
servers = [
    {"ip": "dev.autointelli.com", "username":"root", "password":"@uto!ntelli@123"}
    # Add more servers with credentials
]

# Create Excel workbook and sheet
wb = Workbook()
ws = wb.active
ws.title = "Server Health"

# Headers for Excel file
headers = ["Server IP", "Command", "Output"]
ws.append(headers)

# Gathering server health and writing to Excel
for server in servers:
    health = gather_server_health(server["ip"], server["username"], server["password"])
for command, output in health.items():
        ws.append([server["ip"], command, output])

# Save Excel file
wb.save("server_health_check.xlsx")
