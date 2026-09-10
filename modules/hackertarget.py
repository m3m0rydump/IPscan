import requests

def ht(target):
    url = f"https://api.hackertarget.com/reverseiplookup/?q={target}"
    try:
        response = requests.get(url)
        print("\n")
        print(8*"="+"reverse IP lookup" + 8*"=")
        print(response.text)
    except Exception as Error:
        print("Error: ",Error)
