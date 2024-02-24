from pypsrp.client import Client

hostname = "DevaMuralee"
port = 5985
username = ""
password = ""

# Create the client with NTLM authentication
client = Client(
    hostname,
    username=username,
    password=password,
    port=port,
    ssl=False,  # Set authentication method to NTLM
)

try:
    # Execute PowerShell commands here
    # For example:
    while True:
        pscmd = input("Enter your PowerShell command (or 'e' to exit):")

        if pscmd.lower() == 'e':
            break

        script_result = client.execute_ps(pscmd)
        script_output = script_result[0].strip()
        print("Script Output:")
        print(script_output)

except KeyboardInterrupt:
    pass  # Handle Ctrl+C to exit the loop

finally:
    client.close()
