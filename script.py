import json
import os
from opengraphio import OpenGraphIO

KEY = os.environ.get("OPENGRAPH_API_KEY")

opengraph = OpenGraphIO({ 'app_id': KEY , "timeout": 120})

def readFile(doc):
    result = {}
    with open(doc,"r") as f:
        result = json.load(f)
    return result["sites"]

all_sites = readFile("data.json")

def getUrls(username):
   all_urls = []
   for key, value in all_sites.items():
        new_url = value["url"].replace("}", "").replace("{username", username)
        all_urls.append(new_url)
    
   return all_urls


def getOpengraphData(username):
   sites = {}

   all_urls = getUrls(username)

   for url in all_urls:
    print(url)
    response = opengraph.get_site_info(url)
    if "error" in response.keys():
        pass
    else:
        if "error" in response["openGraph"].keys():
            if "site_name" in response["htmlInferred"].keys():
                name = response["htmlInferred"]["site_name"]
            if 'title' in response["hybridGraph"].keys():
                name = response["hybridGraph"]["title"].split(" ")[:3]
                name = ' '.join(name)
            else:
                arrayName = url.split(".com")
                name = arrayName[0]
            
            sites[name] = {'url': response["hybridGraph"]["url"],
                            "images": response["htmlInferred"]["images"],
                            "title": name,
                            "description": "This site may require login to view information. Check the URL manually for reliability"}
        else:
            response["openGraph"]['url'] = response['url']
            if "site_name" in  response["openGraph"].keys():
                sites[response["openGraph"]["site_name"]] = response["openGraph"]
                sites[response["openGraph"]["site_name"]]["images"] = response["htmlInferred"]["images"]
            else:
                sites[response["htmlInferred"]["site_name"]] = response["openGraph"]
                sites[response["htmlInferred"]["site_name"]]["images"] = response["htmlInferred"]["images"]
   return sites


a = getOpengraphData("dianagureev")
print(a)