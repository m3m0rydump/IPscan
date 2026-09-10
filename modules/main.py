import os
from .checkhost import ping_check, dns_check
from .target_input import ask_ip
from .ip_api import ipapi
from .proxynova import proxynova
from .hackertarget import ht
from .leakcheck import leakcheck
from .scanports import scan
def main_():
    target = ask_ip()
    ipapi(target)
    dns_check(target, max_nodes=3)
    ping_check(target, max_nodes=3)
    ht(target)
    proxynova(target)
    leakcheck(target)
    c = input("scan ports y/n: ")
    if c == "y":
        scan(target)
    else:
        pass