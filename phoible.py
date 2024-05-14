import pandas as pd

# options: only phonemes; w/allophones; w/features
# 'tone', 'stress' -> can have tone / can be stressed

# Создаём словарь с парами вида "аббревиатура источника: название источника" для красивого вывода
inventories_dict = {"aa": "Chanard, C. (2006). Systèmes alphabétiques des langues africaines",
                    "ea": "Nikolaev, Dmitry; Andrey Nikulin; and Anton Kukhto. 2015. The database of Eurasian phonological inventories",
                    "er": "Round, Erich R. 2019. Phonemic inventories of Australia (database of 392 languages)",
                    "ph": "Moran, Steven. (2012). Phonetics Information Base and Lexicon",
                    "ra": "Ramswami, N. 1999. Common Linguistic Features in Indian Languages: Phonetics",
                    "saphon": "Michael, Lev, Tammy Stark, and Will Chang. (2012) South American Phonological Inventory Database",
                    "spa": "Crothers, J. H., Lorentz, J. P., Sherman, D. A., & Vihman, M. M. (1979)",
                    "upsid": "Maddieson, I., & Precoda, K. (1990). Updating UPSID. UCLA Working Papers in Phonetics"}


# Функция, которая выдаёт всю информацию про заправшиваемый язык из базы данных PHOIBLE.
def get_info(language_name: str):
    output_text = "PHOIBLE info:\n\n"

    # languages_info -- датафрейм с информацией про все языки, которые есть в PHOIBLE.
    languages_info = pd.read_csv('https://raw.githubusercontent.com/phoible/dev/master/data/phoible.csv', dtype=str).applymap(str)
    # language_name_info -- датафрейм с информацией только про запрашиваемый язык.
    language_name_info = languages_info[languages_info["LanguageName"].str.lower() == language_name.lower()]

    # Создаём список пар2 (диалект языка, источник, из которого мы достаём информацию про данный диалект).
    dialect_source_list = []
    for i in range(language_name_info.shape[0]):
        if (language_name_info["SpecificDialect"].iloc[i], language_name_info["Source"].iloc[i]) not in dialect_source_list:
            dialect_source_list.append((language_name_info["SpecificDialect"].iloc[i], language_name_info["Source"].iloc[i]))

    # Достаём информацию про каждую пару (диалект - источник) и сводим в один вывод.
    for dialect_source in dialect_source_list:
        # Создаём датафрейм с информацией только про нужный диалект и источник и передаём его в функцию.
        dialect_source_info = language_name_info[(language_name_info["SpecificDialect"] == dialect_source[0]) &
                                                 (language_name_info["Source"] == dialect_source[1])]
        output_text += get_dialect_info(dialect_source_info, language_name, dialect_source[0], dialect_source[1])

    return output_text


# Функция, выдающая информацию про конкретный диалект.
def get_dialect_info(dialect_source_info: pd.DataFrame, language_name: str, dialect: str, source: str):
    # Выводим все три варианта сразу: фонемы; фонемы + аллофоны; фонемы + их характеристики
    if dialect == "nan":
        dialect = "Standard"
    output_text = f"Phonological system of {language_name} ({dialect}). Source: {inventories_dict[source]}.\n\n"

    # Выводим список согласных и гласных сегментов запрашиваемого языка.
    consonants_list = list(dialect_source_info[dialect_source_info["SegmentClass"] == "consonant"]["Phoneme"])
    vowels_list = list(dialect_source_info[dialect_source_info["SegmentClass"] == "vowel"]["Phoneme"])
    output_text += f"Phonemes\nConsonants: {', '.join(consonants_list)}.\nVowels: {', '.join(vowels_list)}.\n\n"

    return output_text


print(get_info("Moloko"))
