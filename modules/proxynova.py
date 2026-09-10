import requests

def proxynova(target):
    try:
        response = requests.get(f"https://api.proxynova.com/comb?query={target}&start=0&limit=15").json()
        data = response
        print("\n")
        print(8*"=" + "proxynova" + 8*"=")
        for key, value in data.items():
            if key == 'count':
                print(f"{key}: {value}")
            elif key == 'lines':
                print(f"{key}:")
                for line in value:
                    print(f"{line}")
    except Exception as e:
        print("Error: ", e)