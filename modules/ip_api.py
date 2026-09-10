import requests

def ipapi(target):
    url = f"http://ip-api.com/json/{target}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
    response = requests.get(url)
    data = response.json()
    try:
        print("\n")
        print(8*"=" + "IP API" + 8*"=")
        for key, value in data.items():
            print(f"{key}: {value}")
    except Exception as Error:
        print("Error: ",Error)