import time
import requests

BASE_URL = "https://check-host.net"
HEADERS = {"Accept": "application/json"}


def _start_check(check_type: str, host: str, max_nodes: int = 3) -> str | None:
    url = f"{BASE_URL}/check-{check_type}"
    params = {"host": host, "max_nodes": max_nodes}

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()

        if "request_id" not in data:
            print(f"[!] Check-Host did not return request_id: {data}")
            return None

        return data["request_id"]

    except requests.RequestException as e:
        print(f"[!] Request to Check-Host failed: {e}")
        return None


def _get_result(request_id: str, retries: int = 6, delay: float = 1.5) -> dict | None:
    url = f"{BASE_URL}/check-result/{request_id}"

    data = None
    for _ in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            data = r.json()

            if data and all(v is not None for v in data.values()):
                return data

        except requests.RequestException as e:
            print(f"[!] Failed to fetch result: {e}")
            return None

        time.sleep(delay)

    return data

def ping_check(target: str, max_nodes: int = 3):
    print(f"\n[*] Ping check: {target}")

    request_id = _start_check("ping", target, max_nodes)
    if not request_id:
        return

    print(f"[*] Request sent (id: {request_id}), waiting for results...")
    results = _get_result(request_id)
    if not results:
        print("[!] Could not get ping results.")
        return

    print()
    for node, data in results.items():
        if data is None:
            print(f"  {node:35} — still checking...")
            continue
        if data and isinstance(data[0], list) and data[0] and isinstance(data[0][0], list):
            data = data[0]

        success = []
        for entry in data:
            if isinstance(entry, list) and entry and entry[0] == "OK":
                success.append(entry)

        total = len(data)
        if success:
            times = [e[1] for e in success if len(e) > 1]
            avg = sum(times) / len(times) if times else 0
            ip = success[0][2] if len(success[0]) > 2 else "?"
            print(f"  {node:35} — {len(success)}/{total} OK, "
                  f"avg {avg * 1000:.1f} ms, IP: {ip}")
        else:
            reason = data[0][0] if data and isinstance(data[0], list) else "UNKNOWN"
            print(f"  {node:35} — 0/{total} OK ({reason})")


def dns_check(target: str, max_nodes: int = 3):

    if not target.startswith(("http://", "https://")):
        target = f"https://{target}"

    print(f"\n[*] DNS check: {target}")

    request_id = _start_check("dns", target, max_nodes)
    if not request_id:
        return

    print(f"[*] Request sent (id: {request_id}), waiting for results...")
    results = _get_result(request_id)
    if not results:
        print("[!] Could not get DNS results.")
        return

    print()
    for node, data in results.items():
        if data is None:
            print(f"  {node:35} — still checking...")
            continue
        if not isinstance(data, dict):
            print(f"  {node:35} — unexpected format: {data}")
            continue

        parts = []
        for record_type, values in data.items():
            if not values:
                continue
            flat = []
            for v in values:
                if isinstance(v, list):
                    flat.append(str(v[0]) if v else "?")
                else:
                    flat.append(str(v))
            parts.append(f"{record_type}={'/'.join(flat)}")
        if parts:
            print(f"  {node:35} — {', '.join(parts)}")
        else:
            print(f"  {node:35} — no records")