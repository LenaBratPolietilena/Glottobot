# Glottobot
_Five weird lil guys doing a big scary project frrr bruhhh_

## Список участников проекта: 
Марат Богаутдинов, Виктория Зубкова, Елена Иванова, Григорий Тихонов (БКЛ 232, группа Таси), Виктория Краснова (БКЛ 231, группа Тёмы)

## Описание проекта:
Данный проект представляет собой телеграм-бот, который собирает данные по заданному пользователем языку (вписывается вручную) и уровню языка (на выбор: _phonetics, morphology, syntax, lexicon_) из четырёх лингвистических баз данных: _WALS_ (все уровни языка), _Grambank_ (все уровни языка), _Glottolog_ (данные выдаются всегда вне зависимости от уровня языка) и _Phoible_ (фонетика). Бот взаимодействует с пользователем на английском языке.

Репозиторий состоит из *README.md* (_вы находитесь здесь_) с основной информацией, файла *requirements.txt* с техническими требованиями к среде для запуска проекта (установленные библиотеки и т. д.), а также из файлов с кодом:
1) Файл _glottobotocode.py_ с кодом для запуска бота
2) Файлов с функциями, позволяющими доставать данные из соответствующих баз: *WALS.py*, *Phoible.py*, *Grambank.py*, *Glottolog.py*

## Инструкция по запуску бота:
Бот работает в телеграм по ссылке: 
https://t.me/glottobot_bot

Бота также можно запустить с локального устройства. Для этого необходимо клонировать репозиторий Glottobot: 
```
git clone https://github.com/LenaBratPolietilena/Glottobot.git
```
Установить необходимые библиотеки из requirements.txt:
```
pip install -r requirements.txt
```
Готово! В целом ботом уже можно пользоваться. 

## Источники данных:
Данные для бота берутся из таблиц, опубликованных в открытых гитхабах соответствующих баз. Ниже ссылки на авторство баз:
  Dryer, Matthew S. & Haspelmath, Martin (eds.) 2013. The World Atlas of Language Structures Online. Jena: Max Planck Institute for the Science of Human History. (Available online at https://wals.info, github: https://github.com/clld/wals3)
  Hammarström, Harald & Forkel, Robert & Haspelmath, Martin & Bank, Sebastian. 2020. Glottolog 4.2.1. Jena: Max Planck Institute for the Science of Human History. (Available online at https://glottolog.org, github: https://github.com/glottolog)
  Moran, Steven & McCloy, Daniel (eds.) 2019. PHOIBLE. Jena: Max Planck Institute for the Science of Human History. (Available online at https://phoible.org, github: https://github.com/phoible)
  
  Skirgård, Hedvig and Haynie, Hannah J. and Blasi, Damián E. and Hammarström, Harald and Collins, Jeremy and Latarche, Jay J. and Lesage, Jakob and Weber, Tobias and Witzlack-Makarevich, Alena and Passmore, Sam and Chira, Angela and Maurits, Luke and Dinnage, Russell and Dunn, Michael and Reesink, Ger and Singer, Ruth and Bowern, Claire and Epps, Patience and Hill, Jane and Vesakoski, Outi and Robbeets, Martine and Abbas, Noor Karolin and Auer, Daniel and Bakker, Nancy A. and Barbos, Giulia and Borges, Robert D. and Danielsen, Swintha and Dorenbusch, Luise and Dorn, Ella and Elliott, John and Falcone, Giada and Fischer, Jana and Ghanggo Ate, Yustinus and Gibson, Hannah and Göbel, Hans-Philipp and Goodall, Jemima A. and Gruner, Victoria and Harvey, Andrew and Hayes, Rebekah and Heer, Leonard and Herrera Miranda, Roberto E. and Hübler, Nataliia and Huntington-Rainey, Biu and Ivani, Jessica K. and Johns, Marilen and Just, Erika and Kashima, Eri and Kipf, Carolina and Klingenberg, Janina V. and König, Nikita and Koti, Aikaterina and Kowalik, Richard G. A. and Krasnoukhova, Olga and Lindvall, Nora L.M. and Lorenzen, Mandy and Lutzenberger, Hannah and Martins, Tônia R.A. and Mata German, Celia and van der Meer, Suzanne and Montoya Samamé, Jaime and Müller, Michael and Muradoglu, Saliha and Neely, Kelsey and Nickel, Johanna and Norvik, Miina and Oluoch, Cheryl Akinyi and Peacock, Jesse and Pearey, India O.C. and Peck, Naomi and Petit, Stephanie and Pieper, Sören and Poblete, Mariana and Prestipino, Daniel and Raabe, Linda and Raja, Amna and Reimringer, Janis and Rey, Sydney C. and Rizaew, Julia and Ruppert, Eloisa and Salmon, Kim K. and Sammet, Jill and Schembri, Rhiannon and Schlabbach, Lars and Schmidt, Frederick W.P. and Skilton, Amalia and Smith, Wikaliler Daniel and de Sousa, Hilário and Sverredal, Kristin and Valle, Daniel and Vera, Javier and Voß, Judith and Witte, Tim and Wu, Henry and Yam, Stephanie and Ye 葉婧婷, Jingting and Yong, Maisie and Yuditha, Tessa and Zariquiey, Roberto and Forkel, Robert and Evans, Nicholas and Levinson, Stephen C. and Haspelmath, Martin and Greenhill, Simon J. and Atkinson, Quentin D. and Gray, Russell D. 2023. Grambank. Jena: Max Planck Institute for the Science of Human History. (Available online at https://grambank.clld.org, github: https://github.com/grambank)
  
