import subprocess
import time
import sys
import os
import socket
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
from tabulate import tabulate
from ipaddress import ip_address

# Initialize colorama for cross-platform support
init(autoreset=True)

def resolve_hostname(host):
    """Resolve hostname to IP address, or return None if unable."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None

def ping_host(host, count):
    try:
        # Determine the parameter for ping count and timeout based on the OS
        if sys.platform.lower().startswith('win'):
            param_count = '-n'
            param_timeout = '-w'  # Timeout in milliseconds
            timeout_value = '1000'  # 1 second = 1000 ms
        else:
            param_count = '-c'
            param_timeout = '-W'  # Timeout in seconds
            timeout_value = '1'  # 1 second

        # Ping the host using the 'ping' command with a timeout
        output = subprocess.run(
            ["ping", param_count, str(count), param_timeout, timeout_value, host], 
            capture_output=True, 
            text=True
        )
        if output.returncode == 0:
            return (host, f"{Fore.GREEN}Online{Style.RESET_ALL}")
        else:
            return (host, f"{Fore.RED}Offline{Style.RESET_ALL}")
    except Exception as e:
        return (host, f"{Fore.YELLOW}Error: {str(e)}{Style.RESET_ALL}")

def ping_hosts_concurrently(hosts, count):
    # Prepare a list to store results, initialized with None
    results = [None] * len(hosts)
    with ThreadPoolExecutor(max_workers=len(hosts)) as executor:
        # Submit tasks and store futures in the same order as hosts
        futures = {executor.submit(ping_host, host, count): idx for idx, host in enumerate(hosts)}
        for future in as_completed(futures):
            idx = futures[future]  # Get the original index of the host
            try:
                result = future.result()
                results[idx] = result  # Store the result in the correct position
            except Exception as e:
                results[idx] = (hosts[idx], f"Error occurred: {e}")
    return results

def clear_screen():
    # Clear command based on the operating system
    os.system('cls' if sys.platform.lower().startswith('win') else 'clear')

def sort_by_ip_and_domain(results):
    """Sort IPs numerically and hostnames alphabetically, placing hostnames at the end."""
    ip_results = []
    domain_results = []

    for host, status in results:
        ip = resolve_hostname(host)
        if ip and ip == host:  # If it's an IP address (not a resolved domain)
            ip_results.append((host, status, ip_address(ip)))
        else:
            # Treat it as a domain (whether it resolves to an IP or not)
            domain_results.append((host, status))

    # Sort the resolved IP addresses numerically
    ip_results.sort(key=lambda x: x[2])

    # Sort hostnames alphabetically by domain name
    domain_results.sort(key=lambda x: x[0])

    # Combine both lists, with IP-sorted results first, then domains
    sorted_results = [(host, status) for host, status, _ in ip_results] + domain_results

    return sorted_results

def display_countdown(interval):
    """Display a countdown in seconds, updating the screen every second."""
    for remaining in range(interval, 0, -1):
        print(f"{Fore.CYAN}Status: Idle (Next ping in {remaining} seconds){Style.RESET_ALL}", end="\r")
        time.sleep(1)

def format_table_multi_column(results):
    """Format the results into multiple columns if screen height is not enough."""
    # Get terminal size
    terminal_size = shutil.get_terminal_size()
    max_rows = terminal_size.lines - 5  # Reserve some rows for headers, status, etc.

    # If the number of hosts fits in one column, just print a single table
    if len(results) <= max_rows:
        return tabulate(results, headers=["Host", "Status"], tablefmt="grid")

    # Split the results into multiple columns
    columns_needed = (len(results) + max_rows - 1) // max_rows  # Round up to determine columns
    column_width = len(results) // columns_needed  # Hosts per column

    # Create rows for the table
    rows = []
    for i in range(max_rows):
        row = []
        for j in range(columns_needed):
            idx = i + j * max_rows
            if idx < len(results):
                row.append(f"{results[idx][0]:<20} {results[idx][1]}")
            else:
                row.append("")  # Empty cell if there are no more hosts
        rows.append(row)

    # Format the table without headers for side-by-side columns
    table = tabulate(rows, tablefmt="grid")
    return table

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

    # Initialize the previous results as an empty table
    previous_table = ""

    # Loop to ping hosts constantly
    while True:
        # If there's a previous result, print it before processing
        if previous_table:
            clear_screen()
            print(f"Pinging hosts at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(previous_table)
            print(f"{Fore.CYAN}Status: Processing...{Style.RESET_ALL}")
        
        # Ping hosts and get new results
        results = ping_hosts_concurrently(hosts, count)

        # Sort the results by IP networks and hostnames
        sorted_results = sort_by_ip_and_domain(results)

        # Format new results into a table with multiple columns if needed
        table = format_table_multi_column(sorted_results)

        # After ping is complete, clear the screen and show the new results
        clear_screen()
        print(f"Pinging hosts at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(table)

        # Update the previous results to the new table
        previous_table = table

        # Show dynamic countdown while waiting for the next round
        display_countdown(interval)
