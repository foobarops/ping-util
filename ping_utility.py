import subprocess
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_host(host, count):
    try:
        # Ping the host using the 'ping' command
        output = subprocess.run(["ping", "-c", str(count), host], capture_output=True, text=True)
        if output.returncode == 0:
            return f"{host} is online"
        else:
            return f"{host} is offline"
    except Exception as e:
        return f"Error pinging {host}: {str(e)}"

def ping_hosts_concurrently(hosts, count):
    with ThreadPoolExecutor(max_workers=len(hosts)) as executor:
        futures = {executor.submit(ping_host, host, count): host for host in hosts}
        for future in as_completed(futures):
            host = futures[future]
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"Error occurred while pinging {host}: {e}")

if __name__ == "__main__":
    # Handle command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py [count] [interval] host1 host2 ... hostN")
        sys.exit(1)
    
    # First parameter: count of pings (default 4)
    try:
        count = int(sys.argv[1])
    except (IndexError, ValueError):
        count = 4
    
    # Second parameter: interval between pings (default 10 seconds)
    try:
        interval = int(sys.argv[2])
    except (IndexError, ValueError):
        interval = 10

    # Rest of the parameters: hosts to ping
    hosts = sys.argv[3:] if len(sys.argv) > 3 else ["google.com", "example.com", "localhost"]

    # Loop to ping hosts constantly
    while True:
        print(f"Pinging hosts at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        ping_hosts_concurrently(hosts, count)

        # Wait for the next interval
        time.sleep(interval)
        print("\n" + "-"*40 + "\n")
