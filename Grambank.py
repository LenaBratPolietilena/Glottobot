import pandas as pd

"""
This module lets user get the real wisdom from Grambank.
User can input his language of choice and different linguistics fields such as "morphology", "syntax", 
"lexicon".
Program will find some information for these fields in the foreseeable future.
"""


def get_the_wisdom_of_grambank(user_language: str, user_field: str):
    
    # changing input format to a processable one
    file_languages_info = pd.read_csv('https://raw.githubusercontent.com/grambank/grambank/master/cldf/languages.csv')
    languages_info = pd.DataFrame(data=file_languages_info)
    languages_info["Name"] = languages_info["Name"].str.lower()

    # checking input
    if user_language in languages_info.values:
        user_code = languages_info.loc[languages_info["Name"] == user_language, "ID"].iloc[0]
    else:
        return 'Unfortunately, Grambank can offer no knowledge concerning ' + user_language.title() + '.'

    # setting questions for particular language fields
    fields = dict()
    fields["morphology"] = ["GB028", "GB030", "GB042", "GB043", "GB044", "GB047", "GB059",
                            "GB070", "GB071", "GB074", "GB075", "GB107", "GB158", "GB159"]
    fields["syntax"] = ["GB020", "GB021", "GB024", "GB025", "GB027", "GB134", "GB147",
                        "GB193", "GB327", "GB328", "GB329", "GB408", "GB409", "GB410"]
    fields["lexicon"] = ["GB041", "GB035", "GB057", "GB333", "GB334", "GB335", "GB336", "GB415"]

    # accessing file with data for every question and every language in the database
    file_main_data = pd.read_csv('https://raw.githubusercontent.com/grambank/grambank/master/cldf/values.csv')
    main_data = pd.DataFrame(data=file_main_data)
    
    # finding the right spot in the database
    x = main_data.loc[main_data["Language_ID"] == user_code].index[0]
    language_info = main_data[x:x+195]

    # getting questions by their codes
    file_questions = pd.read_csv('https://raw.githubusercontent.com/grambank/grambank/master/cldf/parameters.csv')
    questions = pd.DataFrame(data=file_questions)

    # getting answers by their codes
    file_answers = pd.read_csv('https://raw.githubusercontent.com/grambank/grambank/master/cldf/codes.csv')
    answers = pd.DataFrame(data=file_answers)

    # finally getting what we need
    output = "Grambank can offer this knowledge:\n\n"
    
    for question in fields[user_field]:
        if question + "-" + user_code in language_info["ID"].values:
            outp = questions.loc[questions["ID"] == question, "Name"].iloc[0] + '\n'
            value = language_info.loc[language_info["ID"] == question + "-" + user_code, "Value"].iloc[0]
            if value == "?":
                answer = "Unclear"
            else:
                answer = answers.loc[answers["ID"] == question + "-" + value, "Description"].iloc[0].title()
                if answer == "Absent":
                    answer = "No"
                elif answer == "Present":
                    answer = "Yes"
            outp += answer + '\n'
            output += outp
    output += f"\nFor more information visit Grambank: https://grambank.clld.org/"

    return output


def get_field(user_language: str):

    """
    This function gives information about the fields for which your requested language can be found in GramBank
    database.
    :param user_language: a name of requested language.
    :return: The function returns the list of fields for which the data about your requested is present.
    """

    #repeating the process
    
    user_language = user_language.lower()

    file_languages_info = pd.read_csv('https://raw.githubusercontent.com/grambank/grambank/master/cldf/languages.csv')
    languages_info = pd.DataFrame(data=file_languages_info)
    languages_info["Name"] = languages_info["Name"].str.lower()

    fields = dict()
    fields["morphology"] = ["GB028", "GB030", "GB042", "GB043", "GB044", "GB047", "GB059",
                            "GB070", "GB071", "GB074", "GB075", "GB107", "GB158", "GB159"]
    fields["syntax"] = ["GB020", "GB021", "GB024", "GB025", "GB027", "GB134", "GB147",
                        "GB193", "GB327", "GB328", "GB329", "GB408", "GB409", "GB410"]
    fields["lexicon"] = ["GB041", "GB035", "GB057", "GB333", "GB334", "GB335", "GB336", "GB415"]

    file_main_data = pd.read_csv('https://raw.githubusercontent.com/grambank/grambank/master/cldf/values.csv')
    main_data = pd.DataFrame(data=file_main_data)

    if user_language in languages_info.values:
        user_code = languages_info.loc[languages_info["Name"] == user_language, "ID"].iloc[0]

    # checking for information about the language in particular fields
        field_output = list()
        for field in fields["syntax"]:
            if field + "-" + user_code in main_data["ID"].values:
                field_output.append("syntax")
            break
        for field in fields["morphology"]:
            if field + "-" + user_code in main_data["ID"].values:
                field_output.append("morphology")
            break
        for field in fields["lexicon"]:
            if field + "-" + user_code in main_data["ID"].values:
                field_output.append("lexicon")
            break

        return ", ".join(field_output)
    else:
        return f''
