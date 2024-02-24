from pypsrp.client import Client

hostname = "dev.autointelli.com", #192.168.1.8
port = 15985
username =" administration"
password = "@ut0!ntell!@123"
  
client = Client(
    hostname,
    username=username,
    password=password,
    port=port,
    ssl=False
    
)

while True:
    pscmd = input("Enter your PowerShell command (or 'e' to exit):")

    if pscmd.lower() == 'e':
        break

    script_result = client.execute_ps(pscmd)

    script_output = script_result[0].strip()
    print("Script Output:")
    print(script_output)

client.close()