import subprocess
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)

def ping_host(host, count):
    try:
        # Determine the parameter for ping count based on the OS
        param = '-n' if sys.platform.lower().startswith('win') else '-c'
        # Ping the host using the 'ping' command
        output = subprocess.run(["ping", param, str(count), host], capture_output=True, text=True)
        if output.returncode == 0:
            return f"{Fore.GREEN}{host} is online{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}{host} is offline{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.YELLOW}Error pinging {host}: {str(e)}{Style.RESET_ALL}"

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
    # Default values
    count = 4
    interval = 10
    hosts = []

    args = sys.argv[1:]
    idx = 0

    # Parse count if provided
    if idx < len(args) and args[idx].isdigit():
        count = int(args[idx])
        idx += 1

    # Parse interval if provided
    if idx < len(args) and args[idx].isdigit():
        interval = int(args[idx])
        idx += 1

    # Remaining arguments are hosts
    hosts = args[idx:]

    if not hosts:
        print("Usage: python script.py [count] [interval] host1 host2 ...")
        sys.exit(1)

    # Loop to ping hosts constantly
    while True:
        print(f"Pinging hosts at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        ping_hosts_concurrently(hosts, count)

        # Wait for the next interval
        time.sleep(interval)
        print("\n" + "-"*40 + "\n")
