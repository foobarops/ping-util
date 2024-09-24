import subprocess

def ping_host(host):
    try:
        # Ping the host using the 'ping' command
        output = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
        if output.returncode == 0:
            return f"{host} is online"
        else:
            return f"{host} is offline"
    except Exception as e:
        return f"Error pinging {host}: {str(e)}"

def ping_hosts(hosts):
    results = []
    for host in hosts:
        result = ping_host(host)
        results.append(result)
        print(result)
    return results

if __name__ == "__main__":
    # List of hosts to ping
    hosts = ["google.com", "example.com", "192.168.1.1", "localhost"]
    
    # Ping all the hosts and display the results
    ping_hosts(hosts)
