import json
import requests
import urllib.request

# Add self
def downloadAptoide(aptoideName):
    print("Downloading App...")
    response = requests.get(f"http://ws75.aptoide.com/api/7/apps/search/query={aptoideName}/limit=1")
    responseJson = response.json()
    responsePath = responseJson.get("datalist").get("list")[0].get("file").get("path")

    try:
        urllib.request.urlretrieve(f"{responsePath}", f"testApks/{aptoideName}.apk")
    except Exception as e:
        print(e)
        return False

    return True

download("com.netflix.mediaclient")
