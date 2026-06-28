#!/usr/bin/env python3
"""
Nginx Log Analyser
Parses Nginx access logs and shows top requests, IPs, paths, status codes and user agents
"""

from collections import Counter
import re

def analyze_logs(log_file_path):
    ip_counter = Counter()
    path_counter = Counter()
    status_counter = Counter()
    user_agent_counter = Counter()

    log_pattern = re.compile(
        r'^(\d+\.\d+\.\d+\.\d+)'
        r'.*?"(GET|POST|PUT|DELETE|HEAD|OPTIONS) '
        r'(\S+)'
        r' HTTP/\d\.\d"'
        r' (\d{3})'
        r'.*?"([^"]+)"$'
    )

    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as log_file:
            for line in log_file:
                match = log_pattern.search(line)
                if match:
                    ip = match.group(1)
                    path = match.group(3)
                    status = match.group(4)
                    user_agent = match.group(5)

                    ip_counter[ip] += 1
                    path_counter[path] += 1
                    status_counter[status] += 1
                    user_agent_counter[user_agent] += 1

        print("=" * 60)
        print("📊 Nginx Log Analysis Results")
        print("=" * 60)

        print("\n🔝 Top 5 IP addresses with most requests:")
        for ip, count in ip_counter.most_common(5):
            print(f"{ip} - {count} requests")

        print("\n🔝 Top 5 most requested paths:")
        for path, count in path_counter.most_common(5):
            print(f"{path} - {count} requests")

        print("\n🔝 Top 5 response status codes:")
        for status, count in status_counter.most_common(5):
            print(f"{status} - {count} requests")

        print("\n🔝 Top 5 most common user agents:")
        for agent, count in user_agent_counter.most_common(5):
            short_agent = agent[:75] + "..." if len(agent) > 75 else agent
            print(f"{short_agent} - {count} requests")

    except FileNotFoundError:
        print(f"❌ Error: File '{log_file_path}' not found.")
        print("👉 Make sure you have downloaded nginx-access.log in this folder.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    LOG_FILE = "nginx-access.log"
    analyze_logs(LOG_FILE)