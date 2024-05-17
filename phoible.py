"""The phoible module lets user get information about phonological inventories of a requested language's dialects
from PHOIBLE database. It may give away more than one inventory if there are several dialects described in PHOIBLE or
if the particular dialect is described in several sources.
"""

import pandas as pd

# This is a dictionary with pairs "source's abbreveation: source's full name" for a beautiful output.
inventories_dict = {"aa": "Chanard, C. (2006). Systèmes alphabétiques des langues africaines",
                    "ea": "Nikolaev, Dmitry; Andrey Nikulin; and Anton Kukhto. 2015. The database of Eurasian phonological inventories",
                    "er": "Round, Erich R. 2019. Phonemic inventories of Australia (database of 392 languages)",
                    "ph": "Moran, Steven. (2012). Phonetics Information Base and Lexicon",
                    "ra": "Ramswami, N. 1999. Common Linguistic Features in Indian Languages: Phonetics",
                    "saphon": "Michael, Lev, Tammy Stark, and Will Chang. (2012) South American Phonological Inventory Database",
                    "spa": "Crothers, J. H., Lorentz, J. P., Sherman, D. A., & Vihman, M. M. (1979)",
                    "upsid": "Maddieson, I., & Precoda, K. (1990). Updating UPSID. UCLA Working Papers in Phonetics"}


def is_available(language_name: str) -> bool:
    """
    The is_available function checks out whether the user_language is in the database or not.
    :param language_name: the requested name.
    :return: If it is true that the language is in PHOIBLE data base.
    """
    
    languages_info = pd.read_csv('https://raw.githubusercontent.com/phoible/dev/master/data/phoible.csv', dtype=str).applymap(str)
    if language_name.lower() not in list(languages_info["LanguageName"].str.lower()):
        return False
    return True


def get_dialect_info(dialect_source_info: pd.DataFrame, language_name: str, dialect: str, source: str) -> str:
    """
    This function gives information about a phonological inventory of a particular dialect from a particular source.
    :param dialect_source_info: a DataFrame with information about a particular dialect from a particular source.
    :param language_name: a name of the requested language.
    :param dialect: a dialect of the requested language that is being described.
    :param source: a source the info about the dialect comes from.
    :return: A phonological inventory of a particular dialect from a particular source. It returns each inventory in 3 ways: a list of phonemes, a list of phonemes with their allophones, a list of phonemes with their features.
    """

    if dialect == "nan":
        dialect = "Standard"
    output_text = f"Phonological inventory of {language_name} ({dialect}). Source: {inventories_dict[source]}.\n"

    # Output of a list of segments.
    consonants_list = list(dialect_source_info[dialect_source_info["SegmentClass"] == "consonant"]["Phoneme"])
    vowels_list = list(dialect_source_info[dialect_source_info["SegmentClass"] == "vowel"]["Phoneme"])
    output_text += f"List of phonemes:\nConsonants: {', '.join(consonants_list)}.\nVowels: {', '.join(vowels_list)}.\n"

    # Output of a list of segments with their allophones.
    output_text += "List of phonemes with their allophones:\nConsonants: "
    consonants_allophones_list = list(dialect_source_info[dialect_source_info["SegmentClass"] == "consonant"]["Allophones"])
    vowels_allophones_list = list(dialect_source_info[dialect_source_info["SegmentClass"] == "vowel"]["Allophones"])

    for i in range(len(consonants_list)):
        if consonants_allophones_list[i] == "nan":
            consonants_allophones_list[i] = consonants_list[i]
    output_text += ', '.join([f"{consonants_list[i]} /{', '.join(consonants_allophones_list[i].split())}/" for i in range(len(consonants_list))])
    output_text += "\nVowels: "

    for i in range(len(vowels_list)):
        if vowels_allophones_list[i] == "nan":
            vowels_allophones_list[i] = vowels_list[i]
    output_text += ', '.join([f"{vowels_list[i]} /{', '.join(vowels_allophones_list[i].split())}/" for i in range(len(vowels_list))])
    output_text += "\n\n"
    '''
    # Output of a list of segments with their features.
    output_text += "List of phonemes with their characteristics:\nConsonants:\n"

    for consonant in consonants_list:
        consonant_row = dialect_source_info[dialect_source_info["Phoneme"] == consonant]
        output_text += f"{consonant} ({', '.join(consonant_row.columns[consonant_row.isin(['+']).any()].tolist())})\n"
    output_text += "\nVowels:\n"

    for vowel in vowels_list:
        vowel_row = dialect_source_info[dialect_source_info["Phoneme"] == vowel]
        output_text += f"{vowel} ({', '.join(vowel_row.columns[vowel_row.isin(['+']).any()].tolist())})\n"
    output_text += "\n"
    '''
    return output_text


def get_info(language_name: str) -> str:
    """
    This function gives all the info about the phonology of the requested language. It may give away more than one
    inventory if there are several dialects described in PHOIBLE or if the particular dialect is described in several
    sources.
    :param language_name: a name of the language that is requested. Can be written in any case.
    :return: The string with the phonology of the requested language. It returns each inventory in 3 ways: a list of phonemes, a list of phonemes with their allophones, a list of phonemes with their features.
    """

    output_text = "PHOIBLE data:\n\n"

    # languages_info - a dataframe with information about all languages that are described in PHOIBLE.
    languages_info = pd.read_csv('https://raw.githubusercontent.com/phoible/dev/master/data/phoible.csv', dtype=str).applymap(str)
    # Checking if the requested langauge exists in PHOIBLE database
    if language_name.lower() not in list(languages_info["LanguageName"].str.lower()):
        return "0"
    # language_name_info - a dataframe with information about the requested language only.
    language_name_info = languages_info[languages_info["LanguageName"].str.lower() == language_name.lower()]

    # Here we create a set of tuples: (dialect of the language: source we take information from).
    dialect_source_set = set()
    for i in range(language_name_info.shape[0]):
        if (language_name_info["SpecificDialect"].iloc[i], language_name_info["Source"].iloc[i]) not in dialect_source_set:
            dialect_source_set.add((language_name_info["SpecificDialect"].iloc[i], language_name_info["Source"].iloc[i]))

    # Here we get all info about each (dialect, source) pair and put it in one output.
    for dialect_source in dialect_source_set:
        # We create a dataframe only about a particular dialect and source.
        dialect_source_info = language_name_info[(language_name_info["SpecificDialect"] == dialect_source[0]) &
                                                 (language_name_info["Source"] == dialect_source[1])]
        output_text += get_dialect_info(dialect_source_info, language_name, dialect_source[0], dialect_source[1])

    return output_text
