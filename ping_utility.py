import subprocess
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
from tabulate import tabulate

# Initialize colorama for cross-platform support
init(autoreset=True)

def ping_host(host, count):
    try:
        # Determine the parameter for ping count based on the OS
        param = '-n' if sys.platform.lower().startswith('win') else '-c'
        # Ping the host using the 'ping' command
        output = subprocess.run(["ping", param, str(count), host], capture_output=True, text=True)
        if output.returncode == 0:
            return (host, f"{Fore.GREEN}Online{Style.RESET_ALL}")
        else:
            return (host, f"{Fore.RED}Offline{Style.RESET_ALL}")
    except Exception as e:
        return (host, f"{Fore.YELLOW}Error: {str(e)}{Style.RESET_ALL}")

def ping_hosts_concurrently(hosts, count):
    results = []
    with ThreadPoolExecutor(max_workers=len(hosts)) as executor:
        futures = {executor.submit(ping_host, host, count): host for host in hosts}
        for future in as_completed(futures):
            host = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append((host, f"Error occurred: {e}"))
    return results

def clear_screen():
    # Clear command based on the operating system
    os.system('cls' if sys.platform.lower().startswith('win') else 'clear')

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
        # Ping hosts and get results
        results = ping_hosts_concurrently(hosts, count)

        # Clear the screen right before printing new results
        clear_screen()

        print(f"Pinging hosts at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Format results in a table
        table = tabulate(results, headers=["Host", "Status"], tablefmt="grid")
        
        # Print the table
        print(table)
        
        # Wait for the next interval before running the next round of pings
        time.sleep(interval)
        print("\n" + "-"*40 + "\n")
