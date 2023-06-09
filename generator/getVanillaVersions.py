import json

import requests
from lxml import etree

print("---=== AuroraServerLauncher.API Generator Module ===---")
print("Module: getVanillaVersions")
print("Notice: This module is used to get all versions of Minecraft Server from mcversions.net")
input("Press Enter to start...")

jsonModel = {
    "latest": "",
    "versions": {}
}

versionList = []
overallVer = requests.get("https://mcversions.net/").content
print("Version List Got")
overallVerCounter = 1
overallVerAnalysis = etree.HTML(overallVer)
print("Version List Analysed")
while True:
    try:
        version = \
            overallVerAnalysis.xpath(f'/html/body/main/div/div[2]/div[1]/div/div[{overallVerCounter}]/@data-version')[0]
        release_time = overallVerAnalysis.xpath(
            f'/html/body/main/div/div[2]/div[1]/div/div[1]/div[{overallVerCounter}]/p/span[2]/time/@datetime')
        if not release_time:
            release_time = overallVerAnalysis.xpath(f'/html/body/main/div/div[2]/div[1]/div/div[{overallVerCounter}]/div[1]/p/span/time/@datetime')

        specificVer = requests.get(f"https://mcversions.net/download/{version}").content
        specificVerAnalysis = etree.HTML(specificVer)
        wikiUrl = specificVerAnalysis.xpath("/html/body/main/div/div[1]/div[1]/blockquote/footer/p/a/@href")[0]
        downloadUrl = specificVerAnalysis.xpath("/html/body/main/div/div[1]/div[2]/div[1]/a/@href")[0]
        print(f"Version: {version} | Release Time: {release_time[0]} | Wiki URL: {wikiUrl} | Download URL: {downloadUrl}")

        jsonModel["versions"][version] = {"id": version, "releaseTime": release_time[0], "changeLog": wikiUrl, "url": downloadUrl}
        versionList.append(version)
        if version == "1.8":
            break
        overallVerCounter += 1
    except IndexError:
        overallVerCounter += 1
        continue

jsonModel["latest"] = versionList[0]
open("../vanillaVersions.json", 'w', encoding="utf-8").write(json.dumps(jsonModel, indent=4, ensure_ascii=False))
print("---=== Done ===---")