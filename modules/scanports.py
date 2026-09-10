import socket

def scan(target):
    ports = {
        20: "FTP-DATA",
        21: "FTP",
        22: "SSH/SFTP",
        23: "Telnet",
        25: "SMTP",
        43: "WHOIS",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        115: "SFTP",
        123: "NTP",
        143: "IMAP",
        161: "SNMP",
        179: "BGP",
        389: "LDAP",
        443: "HTTPS",
        445: "Microsoft-DS",
        465: "SMTPS",
        514: "SYSLOG",
        515: "Printer",
        587: "SMTP",
        636: "LDAPS",
        993: "IMAPS",
        995: "POP3S",
        1080: "SOCKS",
        1194: "OpenVPN",
        1433: "MS SQL Server",
        1723: "PPTP",
        3128: "HTTP Proxy",
        3268: "LDAP",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        6379: "Redis",
        8080: "HTTP-Alt/Tomcat",
        8443: "HTTPS-Alt",
        10000: "Webmin",
        27017: "MongoDB",
    }
    
    open_ports = []
    for port, service in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.7)
        try:
            result = sock.connect_ex((target, port))
            status = "OPEN" if result == 0 else "closed"
            if result == 0:
                open_ports.append((port, service))
            print(f"port {port:5} [{service:15}]: {status}")
        except Exception as e:
            print(f"error {port}: {e}")
        finally:
            sock.close()
    
    if open_ports:
        print(f"\n[!] Open ports: {len(open_ports)}")
        for port, service in open_ports:
            print(f"  - {port} ({service})")