def glottolog_info(language: str):
    
    import requests
    import json
    import csv

    ans = [str("Here's classification and geographical coordinates of " + language + ":")]

    # getting the code for the url
    with open("glottocodes.csv", "r") as g:
        codes = csv.reader(g, dialect='excel', delimiter=';')
        for code in codes:
            if code[0] == language:
                needed_code = code[1]

    # finding the necessary webpage
    final_link = "https://glottolog.org/resource/languoid/id/" + needed_code + ".json"

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
