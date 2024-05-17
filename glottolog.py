def glottolog_info(user_language: str):
    
    import requests
    import json
    import csv
    import pandas as pd

    ans = [str("Here's classification and geographical coordinates of " + user_language + ":")]

    # getting the code for the url
    languages_info = pd.read_csv('https://raw.githubusercontent.com/phoible/dev/master/mappings/InventoryID-LanguageCodes.csv', dtype=str)
    
    if user_language in languages_info.values:
        user_code = languages_info.loc[languages_info["LanguageName"] == user_language, "Glottocode"].iloc[0]
    else:
        user_code = str()        
        return ("Check the name of the language. Maybe, there's a spelling mistake, or there's no such language in Glottolog.")
            
    # finding the necessary webpage
    final_link = "https://glottolog.org/resource/languoid/id/" + user_code + ".json"

    # downloading the info from the webpage
    final = requests.get(final_link)
    info = json.loads(final.text)

    # turning the info into readable txt
    
    for elem in info:
        if elem == "id":
            ans.append(str("Glottocode: " + info["id"]))
        elif elem == "latitude":
            ans.append(str("Latitude: " + str(info["latitude"])))
        elif elem == "longitude":
            ans.append(str("Longitude: " + str(info["longitude"])))
        elif elem == "classification":
            ans.append("Classification: ")
            num = 1
            for item in info["classification"]:
                ans.append(str(str(num) + "    " + item["name"] + "    To learn more go to " + str(item["url"])))
                num += 1
        elif elem == "newick":
            ans.append(str("Dialects: " + info["newick"])) 
            
    output = '\n'.join(ans)
            
    return output


