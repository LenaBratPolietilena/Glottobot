import requests
import json
import csv
import pandas as pd
import re

def glottolog_info(user_language: str):
    
    ans = [str("Here's classification and geographical coordinates of " + user_language + ":")]

    # This piece of code gets the glottocode of the input language.
    languages_info = pd.read_csv('https://raw.githubusercontent.com/phoible/dev/master/mappings/InventoryID-LanguageCodes.csv', dtype=str)
    
    if user_language in languages_info.values:
        user_code = languages_info.loc[languages_info["LanguageName"] == user_language, "Glottocode"].iloc[0]
    else:
        user_code = str()        
        return 0
            
    # This piece of code compiles a link to the necessary webpage.
    final_link = "https://glottolog.org/resource/languoid/id/" + user_code + ".json"

    # This piece of code downloads the information from the webpage.
    final = requests.get(final_link)
    info = json.loads(final.text)

    # This piece of code turns the data from json into readable txt.
    
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
            
            # This piece of code parses the string containing information about dialects from the json.
            dialects = ""
            s = info["newick"]
            s = s.replace("'", "")
            s = s.replace(":","")
            
            bracket = 0
            new_s = ""
            for i in range(len(s)):
                if s[i] == "[" or s[i] == "]":
                    bracket += 1
                if bracket % 2 == 0 and (s[i] != "1" and s[i] != "-"):
                    new_s += s[i]
                    
            new_s = re.split('[(),]', new_s.replace("]", ""))
            
            final_s = new_s[-2 : 0 : -1]
            
            for dialect in final_s:
                if dialect != "":
                    dialects += dialect[:-1] + ", "  
                    
            ans.append(str("Dialects: " + dialects[:-2])) 
            
    output = '\n'.join(ans)
            
    return output

def is_available(user_language: str):
    '''
    The is_available function checks out whether the user_language is in the database or not.
    '''
    
    languages_info = pd.read_csv('https://raw.githubusercontent.com/phoible/dev/master/mappings/InventoryID-LanguageCodes.csv', dtype=str)
    
    if user_language in languages_info.values:
        return True      
    return False