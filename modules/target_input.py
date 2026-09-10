import ipaddress
import sys

def ask_ip(prompt: str = "Enter IP > ") -> str:

    raw = input(prompt).strip()

    if not raw:
        print("[!] Empty input")
        sys.exit(1)

    try:
        ipaddress.ip_address(raw)
    except ValueError:
        print(f"[!] '{raw}' — invalid IP")
        sys.exit(1)

    return raw
