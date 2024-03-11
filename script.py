import json
import os
from opengraphio import OpenGraphIO

# For deploy
KEY = os.environ.get("OPENGRAPH_API_KEY")

opengraph = OpenGraphIO({ 'app_id': KEY , "timeout": 120})

def readFile():
    result = {}
    with open(f"data.json","r") as f:
        result = json.load(f)
    return result["sites"]

all_sites = readFile()
all_urls = []
sites = {}

def getOpengraphData(username):
   for key, value in all_sites.items():
        new_url = value["url"].replace("}", "").replace("{username", username)
        all_urls.append(new_url)

        print(all_urls)

   for url in all_urls:
    response = opengraph.get_site_info(url)
    print(response)
    if "error" in response.keys():
        pass
    else:
        if "error" in response["openGraph"].keys():
            pass
        else:
            response["openGraph"]['url'] = response['url']

            if "site_name" in response["openGraph"].keys():
                sites[response["openGraph"]["site_name"]] = response["openGraph"]
            else:
                if 'wikipedia' in response["openGraph"]['title'].lower():
                    sites["Wikipedia"] = response["openGraph"]
                    
   return sites