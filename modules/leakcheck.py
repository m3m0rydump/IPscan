import requests

def leakcheck(target):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(f"https://leakcheck.io/api/public?&check={target}", headers=headers).json()
        print("\n")
        print(8*"=" + "leakcheck" + 8*"=")        
        if res.get('success'):
            print(f"\nFound leaks: {res.get('found', 0)}")
            print(f"Fields: {res.get('fields', [])}")
            print("\nSources:")
            for source in res.get('sources', []):
                name = source.get('name', 'NA')
                date = source.get('date', 'NA')
                print(f"{name} - {date}")
        else:
            print(f"Error: {res.get('error')}")
            
    except Exception as Error:
        print("Error: ", Error)