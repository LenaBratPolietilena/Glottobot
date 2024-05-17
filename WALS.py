"""The WALS module lets user get information about various features of requested languages from WALS database."""

import pandas as pd


def get_info(user_language_reply: str, user_field: str):

    """
    This function gives information about a particular language field in a particular language.
    :param user_language_reply: a name of requested language.
    :param user_field: language field, requested by user (from the list: "phonetics", "morphology", "syntax", "lexicon")
    :return: The function returns the list of feature names with their values in text format or report about the absence
    of requested language in the WALS database.
    """

    user_language = user_language_reply.lower()

    # changing input format to a better processable one
    file_languages_info = pd.read_csv('https://raw.githubusercontent.com/cldf-datasets/wals/master/raw/'
                                      'languagesMSD.csv')
    languages_info = pd.DataFrame(data=file_languages_info)
    languages_info["NameNEW"] = languages_info["NameNEW"].str.lower()

    # getting wals_code for checking for values and checking for requested language in WALS database
    if user_language in languages_info.values:
        user_code = languages_info.loc[languages_info["NameNEW"] == user_language, "ID"].iloc[0]
    else:
        # getting read of some extra information that might be present in braces in WALS
        languages_info["NameNEW"] = languages_info["NameNEW"].apply(lambda x: x.split()[0] if "(" in x else x)
        if user_language in languages_info.values:
            user_code = languages_info.loc[languages_info["NameNEW"] == user_language, "ID"].iloc[0]
        else:
            # an output if the language was not found in WALS
            return 0

    # setting chapters for particular language fields
    chapter_types = dict()
    chapter_types["phonetics"] = ["1A", "2A", "3A", "4A", "5A", "6A", "7A", "8A", "9A",
                                  "10A", "11A", "12A", "13A", "14A", "15A", "16A", "17A", "18A", "19A"]
    chapter_types["morphology"] = ["20A", "21A", "22A", "23A", "24A", "25A", "26A", "27A", "28A", "29A", "30A", "31A",
                                   "32A", "33A", "34A", "35A", "36A", "37A", "38A", "39A", "40A", "41A", "42A", "43A",
                                   "44A", "45A", "46A", "47A", "48A", "49A", "50A", "51A", "52A", "53A", "54A", "55A",
                                   "56A", "57A", "65A", "66A", "67A", "68A", "69A", "70A", "71A", "72A", "73A", "74A",
                                   "75A", "76A", "77A", "78A", "79A", "80A"]
    chapter_types["syntax"] = ["58A", "59A", "60A", "61A", "62A", "63A", "64A", "81A", "82A", "83A", "84A", "85A",
                               "86A", "87A", "88A", "89A", "90A", "91A", "92A", "93A", "94A", "95A", "96A", "97A",
                               "98A", "99A", "100A", "101A", "102A", "103A", "104A", "105A", "106A", "107A",
                               "108A", "109A", "110A", "111A", "112A", "113A", "114A", "115A", "116A", "117A",
                               "118A", "119A", "120A", "121A", "122A", "123A", "124A", "125A", "126A", "127A", "128A"]
    chapter_types["lexicon"] = ["129A", "130A", "131A", "132A", "133A", "134A", "135A", "136A", "137A", "138A"]

    # accessing file with data for every chapter and every language in the database
    file_main_data = pd.read_csv('https://raw.githubusercontent.com/cldf-datasets/wals/master/cldf/values.csv')
    main_data = pd.DataFrame(data=file_main_data)

    # getting data for the particular field of the particular language
    user_output = dict()
    for chapter in chapter_types[user_field]:
        if chapter + "-" + user_code in main_data["ID"].values:
            user_output[chapter] = main_data.loc[main_data["ID"] == chapter + "-" + user_code, "Value"].iloc[0]

    # getting descriptions for chapter values
    file_chapters_values = pd.read_csv('https://raw.githubusercontent.com/cldf-datasets/wals/master/raw/'
                                       'domainelement.csv')
    chapters_values = pd.DataFrame(data=file_chapters_values)
    descriptions = dict()
    n = 1
    if len(user_output) != 0:
        for chapter in user_output.keys():
            descriptions[chapter] = chapters_values.loc[chapters_values["id"] == chapter + "-"
                                                        + str(user_output[chapter]), "description"].iloc[0]

    # getting chapter names
    final_output = dict()
    file_chapters_names = pd.read_csv('https://raw.githubusercontent.com/cldf-datasets/wals/master/cldf/chapters.csv')
    chapters_names = pd.DataFrame(data=file_chapters_names)
    if len(user_output) != 0:
        for chapter in descriptions.keys():
            chapter_name = chapters_names.loc[chapters_names["ID"] == chapter.rstrip("A"), "Name"].iloc[0]
            final_output[chapter_name] = descriptions[chapter]

    # turning output into text format
    values = " ".join(final_output)
    keys = " ".join(final_output.keys())
    output = f'Here is the information about {user_language_reply} {user_field}:\n\n'+"\n".join(f'{keys}: {values}'
                                                                                                for keys, values in
                                                                                                final_output.items())

    return output


def get_field(user_language_reply: str):

    """
    This function gives information about the fields for which your requested language can be found in WALS database.
    :param user_language_reply: a name of requested language.
    :return: The function returns the list of fields for which the data about your requested is present.
    """

    user_language = user_language_reply.lower()

    # changing input format to a better processable one
    file_languages_info = pd.read_csv('https://raw.githubusercontent.com/cldf-datasets/wals/master/raw/languagesMSD.csv')
    languages_info = pd.DataFrame(data=file_languages_info)
    languages_info["NameNEW"] = languages_info["NameNEW"].str.lower()

    # setting chapters for particular language fields
    chapter_types = dict()
    chapter_types["phonetics"] = ["1A", "2A", "3A", "4A", "5A", "6A", "7A", "8A", "9A",
                                  "10A", "11A", "12A", "13A", "14A", "15A", "16A", "17A", "18A", "19A"]
    chapter_types["morphology"] = ["20A", "21A", "22A", "23A", "24A", "25A", "26A", "27A", "28A", "29A", "30A",
                                   "31A",
                                   "32A", "33A", "34A", "35A", "36A", "37A", "38A", "39A", "40A", "41A", "42A",
                                   "43A",
                                   "44A", "45A", "46A", "47A", "48A", "49A", "50A", "51A", "52A", "53A", "54A",
                                   "55A",
                                   "56A", "57A", "65A", "66A", "67A", "68A", "69A", "70A", "71A", "72A", "73A",
                                   "74A",
                                   "75A", "76A", "77A", "78A", "79A", "80A"]
    chapter_types["syntax"] = ["58A", "59A", "60A", "61A", "62A", "63A", "64A", "81A", "82A", "83A", "84A", "85A",
                               "86A", "87A", "88A", "89A", "90A", "91A", "92A", "93A", "94A", "95A", "96A", "97A",
                               "98A", "99A", "100A", "101A", "102A", "103A", "104A", "105A", "106A", "107A",
                               "108A", "109A", "110A", "111A", "112A", "113A", "114A", "115A", "116A", "117A",
                               "118A", "119A", "120A", "121A", "122A", "123A", "124A", "125A", "126A", "127A",
                               "128A"]
    chapter_types["lexicon"] = ["129A", "130A", "131A", "132A", "133A", "134A", "135A", "136A", "137A", "138A"]

    file_main_data = pd.read_csv('https://raw.githubusercontent.com/cldf-datasets/wals/master/cldf/values.csv')
    main_data = pd.DataFrame(data=file_main_data)

    # getting wals_code for checking for values and checking for requested language in WALS database
    if user_language in languages_info.values:
        user_code = languages_info.loc[languages_info["NameNEW"] == user_language, "ID"].iloc[0]

        # checking for languages in particular fields
        field_output = list()
        for chapter in chapter_types["phonetics"]:
            if chapter + "-" + user_code in main_data["ID"].values:
                field_output.append("phonetics")
            break
        for chapter in chapter_types["morphology"]:
            if chapter + "-" + user_code in main_data["ID"].values:
                field_output.append("morphology")
            break
        for chapter in chapter_types["syntax"]:
            if chapter + "-" + user_code in main_data["ID"].values:
                field_output.append("syntax")
            break
        for chapter in chapter_types["lexicon"]:
            if chapter + "-" + user_code in main_data["ID"].values:
                field_output.append("lexicon")
            break

        return ", ".join(field_output)
    else:
        languages_info["NameNEW"] = languages_info["NameNEW"].apply(lambda x: x.split()[0] if "(" in x else x)

        if user_language in languages_info.values:
            user_code = languages_info.loc[languages_info["NameNEW"] == user_language, "ID"].iloc[0]

            field_output = list()
            for chapter in chapter_types["phonetics"]:
                if chapter + "-" + user_code in main_data["ID"].values:
                    field_output.append("phonetics")
                break
            for chapter in chapter_types["morphology"]:
                if chapter + "-" + user_code in main_data["ID"].values:
                    field_output.append("morphology")
                break
            for chapter in chapter_types["syntax"]:
                if chapter + "-" + user_code in main_data["ID"].values:
                    field_output.append("syntax")
                break
            for chapter in chapter_types["lexicon"]:
                if chapter + "-" + user_code in main_data["ID"].values:
                    field_output.append("lexicon")
                break
            return ", ".join(field_output)
        else:
            return f''
