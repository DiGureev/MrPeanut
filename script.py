import json
import os
from opengraphio import OpenGraphIO

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

   for url in all_urls:
    response = opengraph.get_site_info(url)
    if "error" in response.keys():
        pass
    else:
        if "error" in response["openGraph"].keys():
            pass
        else:
            response["openGraph"]['url'] = response['url']
            if "site_name" in  response["openGraph"].keys():
                sites[response["openGraph"]["site_name"]] = response["openGraph"]
                sites[response["openGraph"]["site_name"]]["images"] = response["htmlInferred"]["images"]
            else:
                sites[response["htmlInferred"]["site_name"]] = response["openGraph"]
                sites[response["htmlInferred"]["site_name"]]["images"] = response["htmlInferred"]["images"]
                
            sites["images"] = response["htmlInferred"]["images"]
                    
   return sites

a = getOpengraphData("mo_narchi")
print(a)