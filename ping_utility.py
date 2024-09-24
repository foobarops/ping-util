import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def ping_hosts_concurrently(hosts):
    with ThreadPoolExecutor(max_workers=len(hosts)) as executor:
        futures = {executor.submit(ping_host, host): host for host in hosts}
        for future in as_completed(futures):
            host = futures[future]
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"Error occurred while pinging {host}: {e}")

if __name__ == "__main__":
    # List of hosts to ping
    hosts = ["google.com", "example.com", "192.168.1.1", "localhost"]

    # Define the interval (in seconds) between pings
    interval = 10  # Ping every 10 seconds

    # Loop to ping hosts constantly
    while True:
        print(f"Pinging hosts at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        ping_hosts_concurrently(hosts)

        # Wait for the next interval
        time.sleep(interval)
        print("\n" + "-"*40 + "\n")
