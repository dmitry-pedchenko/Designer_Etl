# Designer_Etl
## Описание приложения

Данное приложение разработано для осуществления загрузки из файла формата
Excel в базы данных MySQL и Microsoft SQL. Для работы приложения 
необходим установленный Python 3.6 или выше. Этим приложением можно быстро
и удобно загрузить данные даже не обладая знания программирования. На 
данный момент оно пока существует в консольном виде. Ведется работа над
разработкой оконного приложения.

Основная идея этого приложения состоит в том, что для работы с ним нужно
только составить файл конфигурации загрузки в формате XML. Этот файл потом
откроет система и выполнит действия в соответсвии с этим файлом.

## Оглавление

1. [Установка тебуемых пакетов](#Установка-тебуемых-пакетов)
2. [Информация о структуре проекта](#Информация-о-структуре-проекта)
3. [Информация о логировании](#Логирование)
4. [Структура файла конфигурации](#Структура-файла-конфигурации)
5. [Запуск](#Запуск)
6. [Настройка файла конфигурации](#Настройка-файла-конфигурации)
7. [Теги подключения к базе данных и режимы загрузки](#Теги-подключения-к-базе-данных-и-режимы-загрузки)
8. [Конфигурации режимов работы загрузчика](#Конфигурации-режимов-работы-загрузчика)
    1. [Загрузка из файла Excel без подключения таблицы в БД](#Загрузка-из-файла-Excel-без-подключения-таблицы-в-БД)
        1. [Тег importXml](#Тег-importXml)
        2. [Тег exportTable](#Тег-exportTable)
    1. [Загрузка из файла Excel с подключением таблицы в БД](#Загрузка-из-файла-Excel-с-подключением-таблицы-в-БД)
        1. [Тег withDict](#Тег-withDict)
    1. [Режим сравнения двух файлов Excel](#Режим-сравнения-двух-файлов-Excel)
        1. [Тег linkedColumns](#Тег-linkedColumns)
    1. [Режим обновления записей в БД](#Режим-обновления-записей-в-БД)
9. [Пример загрузки](#Пример-загрузки)




## Установка тебуемых пакетов

Для установки требуемых пакетов выполните в консоли следующие команды: 
```
pip install pandas
pip install pymssql
pip install mysql-connector-python
pip install xlrd
```

Если возникают пробоемы с установкой pymssql на MAC OS

В терминале из директории /Applications/Utilities/ пишем

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

затем 

```
brew install freetds
brew link --force freetds
pip install pymssql
```

Это должно решить проблему

---
[:arrow_up:Оглавление](#Оглавление)
## Информация о структуре проекта

В пакет приложения входят следующие директории:
- config
- Core
    - DAO
    - Logger
    - Parser
    - Query
    - Validate
- log
- Source

Директория `config` служит для хранения файлов конфигурации загрузки. 
Файлы конфигурации должны быть в формате `ИМЯ.xml` и должны лежать в корне данной директории

В директории `Core` лежат все скрипты программы. Рассмотрим каждую 
директорию в отдельности

`DAO` директория в которой хранятся классы работы с источником и целевой
базой данных

`Logger` директория в которой хранятся классы работы с логированием

`Parser` директория в которой хранятся классы работы с парсингом опций 
командной строки а также класс парсинга конфигурационного файла

`Query` директория в которой хранятся классы с основной логикой работы 
программы

`Validate` директория в которой хранятся классы с реализацией валидации.
Валидация включает в себя следующие этапы:
- Валидация корректноси составления файла конфигурации
- Валидация доступности требуемых ресурсов (Файла источника и базы данных)
- Валидация данных из файла источника

`log` директория в которую пишутся логи работы системы. Если данная диреткория
отсутствует то она будет создана автоматически, об этом будет свидетельствовать
сообщение в консоли. Для каждого запуска программы в папке `log` создается
отдельная папка в формате `ГОД_МЕСЯЦ_ДЕНЬ_ЧАС_МИНУТА_СЕКУНДА_['ИМЯ ЗАПУЩЕННОГО КОНФИГА']`  

`Source` директория в которой размещаются файлы с данными для загрузки. 
Расширение файлов должно быть *.xlsx* и желательно чтобы файлы были в данном
формате изначально а не пересохраненными. Файлы должны лежать в корне данной папки.

---
[:arrow_up:Оглавление](#Оглавление)

## Логирование


В папке с логами для каждого запуска создается два файла 
- debug.txt
- log.txt

Файл `debug.txt` служит для просмотра ошибок и тестовых сообщений, которые
формируются в процессе выполнения скрипта. Эти сообщения зависят от режима
работы скрипта. Существует два режима работы *test_mode = true* и 
 *test_mode = false* .О режимах работы скрипта будет написано позже. Сейчас просто
приведутся примеры вывода информации в этот файл:

```
2019-09-05 19:06:23,038 - ETL - INFO - Starts executing... NAME.xml
2019-09-05 19:06:23,206 - ETL - INFO - Success open excel file: <NAME.xlsx> on page name: <PAGE_NAME>, list number: <1>
2019-09-05 19:06:23,269 - ETL - INFO - Success connection to host: <DB_HOST>, port: <1433>, database name: <DB_NAME>
2019-09-05 19:06:23,269 - ETL - INFO - Begin validating files...
2019-09-05 19:06:23,274 - ETL - INFO - Validate success...
2019-09-05 19:06:23,274 - ETL - INFO - Loading in db begin...
2019-09-05 19:06:23,275 - ETL - INFO - Test mode: <true>
2019-09-05 19:06:23,284 - ETL - INFO - Rows readed: 0%
2019-09-05 19:06:23,284 - ETL - DEBUG - Debug <0> -  - INSERT INTO [TABLE] ( COLUMN ) VALUES  ( 'VALUE' ); 

...

2019-09-05 19:06:23,381 - ETL - INFO - Rows readed: 25%
2019-09-05 19:06:23,381 - ETL - DEBUG - Debug <0> -  - INSERT INTO [TABLE] ( COLUMN ) VALUES  ( 'VALUE' ); 

...

2019-09-05 19:06:23,470 - ETL - INFO - Rows readed: 50%
2019-09-05 19:06:23,471 - ETL - DEBUG - Debug <0> -  - INSERT INTO [TABLE] ( COLUMN ) VALUES  ( 'VALUE' ); 

...

2019-09-05 19:06:23,566 - ETL - INFO - Rows readed: 75%
2019-09-05 19:06:23,567 - ETL - DEBUG - Debug <0> -  - INSERT INTO [TABLE] ( COLUMN ) VALUES  ( 'VALUE' );  

...

2019-09-05 19:06:23,654 - ETL - INFO - Rows readed: 100%
2019-09-05 19:06:23,654 - ETL - DEBUG - Debug <0> -  - INSERT INTO [TABLE] ( COLUMN ) VALUES  ( 'VALUE' ); 

...

2019-09-05 19:06:23,654 - ETL - INFO - Created <1218> test queries
2019-09-05 19:06:23,654 - ETL - INFO - Log files created in: </FOLDER/Designer_Etl/log/2019_09_05_19_06_23_['NAME.xml']>
2019-09-05 19:06:23,654 - ETL - INFO - Ends executing... successfully completed <NAME.xml>
---
2019-09-05 19:06:23,656 - ETL - INFO - Connection to DB closed
```
Строки с логами имеют следующий вид:

`ГОД-МЕСЯЦ-ДЕНЬ ЧАС:МИНУТА:СЕКУНДА - ETL - УРОВЕНЬ_СООБЩЕНИЯ (INFO / DEBUG / ERROR) - СООБЩЕНИЕ`

Первая строка в логе говорит то, что начался процесс загрузки с конфигурацией NAME.xml
Затем сообщение о том что открылся файл NAME.xlsx. Потом сообщение о том что
произошло подключение к базе данных DB_NAME. Затем начался процесс проверки
корректности данных *Begin validating files...* 
Затем появляется сообщение о том что проверка данных прошла успешно
Следующее сообщение говорит о том что начался процесс обработки данных и загрузки.
Но так как этот лог приведен для примера загрузки в режиме *test_mode = true* 
то в этом режиме не происходит загрузка в саму базу а происходит только 
формирование тестовых строк с запросами к базе данных, для того чтобы
пользователь имел возможность проверить корректность данных. Эти тестовые 
запросы пишутся в файл лога *debug.txt* . Следующая строка *Test mode: <true>*
сообщает о то что программа запущена в режиме *test_mode = true*. Далее идет
секция с выводом тестовых запросов к базе данных. Данная система загрузки
работает в двух режимах: режиме вставки в базу данных (insert) а также 
в режиме обновления записей в базе данных (update). Данный лог представлен
для режима *insert*. Строка с сообщением:
```
Rows readed: 0%
Rows readed: 25%
Rows readed: 50%
Rows readed: 75%
Rows readed: 100%
```
говорит о том, сколько строк обработано в файле источнике по отношению к
общему значению срок в файле
После сообщений с тестовыми строками идет сообщение о том сколько было cформировано
строк с тестовыми запросами к базе `Created <1218> test queries`
Затем идет сообщение о том что выполнение процесса обработки строк закончено и
указывается где были сформированы файла с логами.
Затем, если больше файлов с конфигурациями нет (можно запускать на выполнение
сразу несколько файлов, как это сделать будет показано далее) идет сообщение о том что 
закрывается связь с базой данных `Connection to DB closed`

Для режима *test_mode = fase* логи в файле *debug.txt* выглядят следующим образом:

```
2019-09-05 13:26:12,658 - ETL - INFO - Starts executing... NAME.xml
2019-09-05 13:26:14,174 - ETL - INFO - Success open excel file: <NAME.xlsx> on page name: <Лист1>, list number: <1>
2019-09-05 13:26:14,190 - ETL - INFO - Success connection to host: <DB_HOST>, port: <1433>, database name: <DB_NAME>
2019-09-05 13:26:14,190 - ETL - INFO - Begin validating files...
2019-09-05 13:26:14,190 - ETL - INFO - Validate success...
2019-09-05 13:26:14,205 - ETL - INFO - Loading in db begin...
2019-09-05 13:26:14,205 - ETL - INFO - Test mode: <false>
2019-09-05 13:26:14,205 - ETL - INFO - Rows readed: 0%
2019-09-05 13:26:14,815 - ETL - DEBUG - Debug <1> - Error in database while commiting query:
Row number:<350>
Query: 
                            <INSERT INTO TABLE (  COLUMN ) VALUES  (  'VALUE'  ); >
Message - 
<b"ERROR_MESSAGE_1">

...

2019-09-05 13:26:15,205 - ETL - INFO - Rows readed: 25%
2019-09-05 13:26:15,815 - ETL - DEBUG - Debug <1> - Error in database while commiting query:
Row number:<350>
Query: 
                            <INSERT INTO TABLE (  COLUMN ) VALUES  (  'VALUE'  ); >
Message - 
<b"ERROR_MESSAGE_2">

...

2019-09-05 13:26:16,205 - ETL - INFO - Rows readed: 50%
2019-09-05 13:26:17,205 - ETL - INFO - Rows readed: 75%
2019-09-05 13:26:18,205 - ETL - INFO - Rows readed: 100%
2019-09-05 13:26:50,096 - ETL - DEBUG - Debug <0> -  - 

DEBUG OVERALL

2019-09-05 13:26:50,096 - ETL - DEBUG - Debug <0> -  - 

 -----------------
DEBUG MESSAGE FROM DATABSE

b"ERROR_MESSAGE_1"

NUMBER OF ENTRIES :
 262
-----------------

2019-09-05 13:26:50,096 - ETL - DEBUG - Debug <0> -  - 

 -----------------
DEBUG MESSAGE FROM DATABSE

b"ERROR_MESSAGE_2"

NUMBER OF ENTRIES :
 122
-----------------

2019-09-05 13:26:50,096 - ETL - INFO - Inserted: <18071>; Rows lost: <1054>
2019-09-05 13:26:50,096 - ETL - INFO - Log files created in: <C:\excel_designer\log\2019_09_05_13_26_12_['RefAffair.xml']>
2019-09-05 13:26:50,096 - ETL - INFO - Ends executing... successfully completed <NAME.xml>
---
2019-09-05 13:26:50,096 - ETL - INFO - Connection to DB closed

```
структура сообщений в целом такая же как и при режиме *test_mode = true*
Отличие начинается со строки 8. Тут сообщения об ошибках являются необязательными
Они возникают только тогда когда имеют место ошибки встаки значений в базу данных
Сообщение об ошибке имеет следующий вид:
Оно начинается со строки
`Debug <1> - Error in database while commiting query:`
Затем идет сообщение о номере строки
`Row number:<Номер строки>`
Затем на следующей строке идет сообщение
`Query: `
После которого на следующей строке идет запрос к базе данных на котором
произошла ошибка
После строки с запросом к базе данных идет строка
`Message - `
Которая сообщает о том что на следующей строке будет выведено сообщение от
базы даных `<b"СООБЩЕНИЕ ОБ ОШИБКЕ ОТ БАЗЫ ДАННЫХ">`

После того как будет выведена строка *Rows readed: 100%* процесс загрузки
в базу данных будет завершен. Строка *DEBUG OVERALL* сообщает о том что
далее будет выведена информация об ошибках (если таковые имеются). Эта информация
имеет следующий вид:

```
 -----------------
DEBUG MESSAGE FROM DATABSE

b"СООБЩЕНИЕ ОТ БАЗЫ ДАННЫХ"

NUMBER OF ENTRIES :
 КОЛИЧЕСТВО ОШИБОК
-----------------
```
таким образом, выводится информация по каждой возникшей ошибке: текст ошибки и
количество ошибок с этим текстом возникших при загрузке.

После информации о ошибках при загрузке идет строка 

```
Inserted: <КОЛИЧЕСТВО ВСТАВЛЕННЫХ СТРОК>; Rows lost: <КОЛИЧЕСТВО СТРОК НЕ ВСТАВЛЕННЫХ>
```

Затем идет строка сообщающая о том где созданы файлы с логами. Послен нее
сообщается об окончании выполнения данного конфига. И, если больше не осталось файлов конфигурации в очереди,
сообщение о том что соединение с базой закрывается.

В файл *log.txt* идут только те сообщения, у которых уровень равен *INFO*

Этот файл нужен для того, что можно было посмтореть в целом на процесс выполнения загрузки, не отвлекаясь на сообщения об ошибках.

---
[:arrow_up:Оглавление](#Оглавление)

## Структура файла конфигурации
В директории *config* лежит файл CONFIG.xml который представляет из себя
канонический файл конфигурации.
```xml
<?xml version="1.0"?>

<main>
    <dbtype></dbtype> <!-- mssql/mysql -->
    <dbHost></dbHost> <!-- host ip / name-->
    <dbUser></dbUser> <!-- user -->
    <dbPass></dbPass> <!-- password -->
    <dbBase></dbBase> <!-- database name -->
    <dbPort></dbPort> <!-- port -->
    <loadMode></loadMode> <!-- insert / update -->
    <dict></dict> <!-- true/ false -->
    <checkMode></checkMode> <!-- true/false -->

    <importXml> <!-- configure source excel file -->
        <path></path> <!-- Excel file name.xlsx -->
        <sheetNumber></sheetNumber> <!-- List number in excel [1... ] -->

        <columns>

            <column>
                <colName></colName> <!-- column name in excel -->
                <colNameDb></colNameDb> <!-- colum name in db -->
                <colType></colType> <!-- str / int / float / date-->
                <isPK></isPK> <!-- true/ false -->
                <cropEnd mode="false"></cropEnd> <!-- <cropEnd mode="true/ false">value</cropEnd> -->
                <addValueEnd mode="false"></addValueEnd> <!-- <addValueEnd mode="true/ false">value</addValueEnd> -->
                <takeFromBegin mode="false"></takeFromBegin> <!-- <takeFromBegin mode="true/ false">value</takeFromBegin> -->
                <cropBegin mode="false"></cropBegin> <!-- <cropBegin mode="true/ false">value</cropBegin> -->
                <addValueBegin mode="false"></addValueBegin> <!-- <addValueBegin mode="true/ false">value,value</addValueBegin> -->
                <addValueBoth mode="false"></addValueBoth> <!-- <addValueBoth mode="true/ false">value</addValueBoth> -->
                <replace mode="false">                    <!-- <replace mode="true/ false">value</replace> -->

                    <replaceVal>
                        <value></value>                     <!--value-->
                        <toValue></toValue>                 <!--value-->
                    </replaceVal>

                    <!--...-->

                </replace>
                <filter mode="true">
                    
                    <f_cropEnd mode="false"></f_cropEnd> <!-- <cropEnd mode="true/ false">value</cropEnd> -->
                    <f_addValueEnd mode="false"></f_addValueEnd> <!-- <addValueEnd mode="true/ false">value</addValueEnd> -->
                    <f_takeFromBegin mode="false"></f_takeFromBegin> <!-- <takeFromBegin mode="true/ false">value</takeFromBegin> -->
                    <f_cropBegin mode="false"></f_cropBegin> <!-- <cropBegin mode="true/ false">value</cropBegin> -->
                    <f_addValueBegin mode="false"></f_addValueBegin> <!-- <addValueBegin mode="true/ false">value,value</addValueBegin> -->
                    <f_addValueBoth mode="false"></f_addValueBoth> <!-- <addValueBoth mode="true/ false">value</addValueBoth> -->
                
                    <filterVal>
                        <filterMode></filterMode>      <!-- != = > < <= >= -->
                        <filterValue></filterValue>    <!-- value -->
                    </filterVal>

                    <!-- ...  -->

                </filter>
                <post-filter mode="true">
                    <postfilterVal>
                        <filterMode></filterMode>      <!-- != = > < <= >= -->
                        <filterValue></filterValue>    <!-- value -->
                    </postfilterVal>

                    <!-- ...  -->

                </post-filter>
            </column>

        <!--<column>-->
            <!--...-->
        <!--</column>-->
        <!--...-->
        <!--<column>-->
            <!--...-->
        <!--</column>-->


        </columns>


        <linkedColumns mode="false"> <!-- <linkedColumns mode="true / false"> -->
        <!--only for check mode-->
            <pathToLinkFile></pathToLinkFile> <!-- excel file name.xlsx -->
            <linkedFileSheetNumber></linkedFileSheetNumber> <!-- List number in excel [1... ] -->
            <both></both>                                   <!-- true / false -->

            <column>
                <linkedColName></linkedColName> <!-- column name in excel file to compare -->
                <colNameInSource></colNameInSource> <!-- column name in source excel -->
            </column>

        <!--<column>-->
            <!--...-->
        <!--</column>-->
        <!--...-->
        <!--<column>-->
            <!--...-->
        <!--</column>-->

        </linkedColumns>

        <withDict mode="false"> <!-- true/ false" -->

            <tables>

                <table>
                    <dictTableName></dictTableName> <!-- table name in data base -->
                    <indxDbColumn>indx_1</indxDbColumn> <!-- index column name in receiver -->
                    <indxColumnDic>indx</indxColumnDic> <!-- index column name in dictionary -->

                        <columns>

                            <column>
                                <colName></colName> <!-- column name in excel -->
                                <colNameDb></colNameDb> <!-- colum name in db -->
                                <colType></colType> <!-- str / int / float / date -->
                                <cropEnd mode="false"></cropEnd> <!-- <cropEnd mode="true/ false">value</cropEnd> -->
                                <addValueEnd mode="false"></addValueEnd> <!-- <addValueEnd mode="true/ false">value</addValueEnd> -->
                                <takeFromBegin mode="false"></takeFromBegin> <!-- <takeFromBegin mode="true/ false">value</takeFromBegin> -->
                                <cropBegin mode="false"></cropBegin> <!-- <cropBegin mode="true/ false">value</cropBegin> -->
                                <addValueBegin mode="false"></addValueBegin> <!-- <addValueBegin mode="true/ false">value</addValueBegin> -->
                                <addValueBoth mode="false"></addValueBoth> <!-- <addValueBoth mode="true/ false">value</addValueBoth> -->
                                <replace mode="false">                    <!-- <replace mode="true/ false">value</replace> -->

                                <replaceVal>
                                    <value></value>                     <!--value-->
                                    <toValue></toValue>                 <!--value-->
                                </replaceVal>

                                <!--...-->

                                </replace>
                            </column>

                        <!--<column>-->
                        <!--...-->
                        <!--</column>-->
                        <!--...-->
                        <!--<column>-->
                        <!--...-->
                        <!--</column>-->

                        </columns>
                </table>

            <!--<table></table>-->
            <!---->
            <!--...-->
            <!---->
            <!--<table></table>-->


            </tables>
        </withDict>

    </importXml>

    <exportTable> <!-- configure receiver data base columns -->
        <path></path>            <!-- receiver data base table name [dbo].[name] -->

        <columns>

            <column>
                <name></name>                                <!-- column name in database -->
                <fromExcel></fromExcel>                  <!-- true/ false -->
                <fromDb></fromDb>                       <!-- true/ false -->
                <isAutoInc></isAutoInc>                 <!-- true/ false -->
                <isConc></isConc>                       <!-- true/ false -->
                <defaultValue mode="false"></defaultValue>   <!-- <defaultValue mode="false/tue">value</defaultValue> -->
                <colType></colType>                       <!-- str / int -->
                <isUpdateCondition></isUpdateCondition> <!-- true/ false -->
                <ifNull mode="false"></ifNull>               <!-- mode =  true/ false -->
            </column>

        <!--<column>-->
        <!--...-->
        <!--</column>-->
        <!--...-->
        <!--<column>-->
        <!--...-->
        <!--</column>-->

        </columns>
    </exportTable>
</main>
```

---
[:arrow_up:Оглавление](#Оглавление)

## Запуск

Для запуска скрипта необходимо выполнить следующие шаги: 
Открыть консоль и зайти в корень директории с проектом, проще всего 
сделать это следующим образом: открываете в проводнике папку с проектом, заходите
в директорию и выделив и удалив строку вверху где прописан путь до папки
написать *cmd* и нажать *enter* таким образом откроется консоль сразу в нужной папке
затем в консли нужно прописать следующую команду 
```
python Main_excel_parser.py --test_mode true/false --config name.xml 
```
первые две команды всегда одни и теже а вот третья и четвертая это режим работы программы
и имя файла конфигурации для данной загрузки. После *--test_mode* необходимо указать
true или false в зависимости от нужного режима загрузки. А также после *--config* нужно
указать имя файла конфигурации.


| Опция | Значение |
|-------|---------|
| --test_mode true | Запуск в режиме отладки |
| --test_mode false| Запуск в режиме загрузки в базу |
| --config конфигуратор.xml | Загрузка с выполением одного файла конфигурации |
| --config конфигуратор1.xml конфигуратор2.xml и т.д. | Загрузка с выполением нескольких файлов конфигурации |


---
[:arrow_up:Оглавление](#Оглавление)

## Настройка файла конфигурации

### Описание

В папке сonfig лежит файл CONFIG.xml это файл конфигурации который служит для понимания структуры конфигурации. В нем
лежит структура файла конфигурации в общем виде

Файл конфигуратор представляет собой файл для настроек загрузки из файла excel в базу данных
файл имеет слудующую структуру:
каждое значение заключено в теги вида  
```xml
<имя_ега>значение</имя_ега>
```
также у некоторых тегов есть свойства вида 
```xml
<имя_ега mode="значение свойства">значение</имя_ега>
```
значение свойства бывают либо `false` либо `true`
если хотите указать число то пишите число в тег, если даже строку то пишите просто строку без ковычек то есть  

~~<имя_ега>'значение'</имя_ега>~~ 

о предназначении свойств будет рассказано далее

конфигратор имеет следующее древовидное значение:

---
[:arrow_up:Оглавление](#Оглавление)
## Информация о структуре проекта

### Теги подключения к базе данных и режимы загрузки
```xml
    <dbtype></dbtype> mssql/mysql
    <dbHost></dbHost> имя хоста базы
    <dbUser></dbUser> имя пользователя базы
    <dbPass></dbPass> пароль от пользователя
    <dbBase></dbBase> имя базы
    <dbPort></dbPort> порт
    <loadMode></loadMode> <!-- insert / update -->
    <dict></dict> <!-- true/ false -->
    <checkMode></checkMode> <!-- true/false -->
```

|тег|значение|
|---|---|
|dbHost|хост базы данных|
|dbUser|пользователь под которым подключаемся к БД|
|dbPass|Пароль от пользователя|
|dbBase|Имя БД|
|dbPort|Порт по которому подключаемся к БД|
|dbtype|Тип базы данных|
|loadMode|режим загрузки: для вставки insert для апдейта update|
|dict|ставится true если загрузка осуществляется при помощи словарной таблицы из базы, если только грузится из эекселя то ставим false|
|checkMode|если указано true то загрузчик превращается в сравниватель таблиц Excel а если false то программа работает в режиме загрузчика|

|тип базы|значение в теге|
|---|---|
|Microsoft SQL|mssql|
|MySQL|mysql|

---
[:arrow_up:Оглавление](#Оглавление)

## Информация о структуре проекта

##  Конфигурации режимов работы загрузчика

Далее рассмотрим два варианта работы загрузчика. Они настраиваются в теге 
```xml
<loadMode></loadMode>
```

## Загрузка из файла Excel без подключения таблицы в БД

Тег loadMode = insert и checkMode = false; dict = false

Рассмотрим сначала вариант

`<loadMode>insert</loadMode>`

При этом условимся то что

```xml
<checkMode>false</checkMode> 
<dict>false</dict>
```

Данная условность говорит о том, что загрузка происходит в БД напрямую из файла
Описанные ниже теги всегда присутсвуют в файле конфигурации независимо от конфигурации базы и файла источника данных для данного вида загрузки

```xml
<?xml version="1.0"?>

<main>
    <dbtype></dbtype> mssql/mysql
    <dbHost></dbHost> имя хоста базы
    <dbUser></dbUser> имя пользователя базы
    <dbPass></dbPass> пароль от пользователя
    <dbBase></dbBase> имя базы
    <dbPort></dbPort> порт
    <loadMode>insert</loadMode> <!-- insert / update -->
    <dict>false</dict> <!-- true/ false -->
    <checkMode>false</checkMode> <!-- true/false -->
   

    <importXml>                в этом блоке лежат блоки описания источников для полей базы
        <path></path>          имя файла excel из которого будет идти загрузка
        <sheetNumber>1</sheetNumber>   номер страницы на которой нужно открыть excel, нумерация с 1

        <columns>              
        	{тут лежит список колонок источников для базы}
        </columns>
        
        <linkedColumns mode="false"></linkedColumns>
        <withDict mode="false"></withDict>
        
    </importXml>
    
    
    
    
    <exportTable>              в этом блоке лежат блоки описания полей базы данных
        <path>[dbo].[имя_таблицы]</path>   имя таблицы в базе
        <columns>
        	{тут лежит список колонок в базе данных}
        </columns>
    </exportTable>
</main>
```

---
[:arrow_up:Оглавление](#Оглавление)

## Информация о структуре проекта
##### Тег importXml
Смысл этого блока в том, что он сожержит данные об источнике данных (файле Excel)
тег `path` содержит в имя файла Excel. Имя файла должно обязательно содержать в себе расширение .xlsx (.xls опционально)
тег sheetNumber сожержит в себе номер страницы на которой необходимо открыть файл с данными

далее идет тег columns которых содержит в себе теги `column`, их может быть сколь угодно много. 

Опишем содержимое тега column
```xml
<column>
    <colName>имя_колонки_в_файле</colName>
    <colNameDb>имя_поля_в_базе</colNameDb>
    <colType>тип_колонки_в_файле</colType>
    <isPK>true_или_false_признак_первичного_ключа</isPK>
    <cropEnd mode="false\true">значение(число)</cropEnd>
    <addValueEnd mode="false\true">значение(строка)</addValueEnd>
    <takeFromBegin mode="false\true">значение(число)</takeFromBegin>
    <cropBegin mode="false\true">значение(число)</cropBegin>
    <addValueBegin mode="false\true">значение(строка)</addValueBegin>
    <addValueBoth mode="false\true">значение(строка),значение(строка)</addValueBoth>
    <replace mode="false\true"></replace>
    <filter mode="false\true"></filter>
</column>
```
выше указанный набор тегов должен быть указан всегда даже если какие-то теги не используются
у некоторых тегов есть свойство `mode=""` это свойство нужно для того чтобы указать работает ли данный
тег или нет, если работает то пишется *true* и ставится занчение в тег или тег выключен то пишется *false* и оставляется пустым тег

теперь обо всем по порядку

|тег|значение|
|---|---|
|colName|указывает для какой колонки в базе этот блок|
|colNameDb|указывает в какое поле в базе идут данные из этой колонки он должен быть равен одному из тегов name из блока exportTable|
|colType|описывает к какому типу будет преобразовано значение из этой колонки. Принимает значение int str float date|
|isPK|тег нужен для проверки колонки на уникалоность значений в колонке в источнике. true или false|

далее идут теги со свойствами. 

|тег|значение|
|---|---|
|cropEnd|принимает значением только число и обрезает указанное значение от конца строки|
|addValueEnd|добавляет строку после значения из поля|
|takeFromBegin|принимает как значение число,он берет начало строки до указанного значения|
|cropBegin|принимает как значение число. Этот тег возращает строку начиная с этого числа до конца строки|
|addValueBegin|принимает на вход строку. Этот тег добавляет в начала строки строку указанную в теге|
|addValueBoth|принимает две строки на вход через запятую. Этот тег добавляет первую строчку в начало строки а вторую в конец|
|replace|отвечает за замену значения на другое значение|
|filter|фильтрация поля по значению до преобразования поля. В том числе и даты.|
|post-filter|фильтрация поля по значению после преобразования поля|

##### cropEnd

принимает значением только число и обрезает указанное значение от конца строки, например если вы хотите включить данный тег то указываете
в свойстве значение я true (это относится ко всем тегам со свойствами) например
<cropEnd mode="true">2</cropEnd>
если вам не нужен этот тег то оставляете как есть
<cropEnd mode="false"></cropEnd>
смысл работы данного тега такой: если например у вас попала строка "Привет" и вы включили этот тег и указали 2 то в результате строка превратится в "Приве"


##### addValueEnd

добавляет строку после значения из поля, например если вы указали <addValueEnd mode="true"> мир!</addValueEnd> (пробелы сохраняются) и попалась 
строка "Привет" то в результате получится "Привет мир!"

##### takeFromBegin

принимает как значение число,он берет начало строки до указанного значения. Например если строка "Привет" а в теге 2 то получится на выходе "Пр"

##### cropBegin

принимает как значение число. Этот тег возращает строку начиная с этого числа до конца строки, например "Привет" а в теге 2 то получится на выходе "ивет"

##### addValueBegin

принимает на вход строку. Этот тег добавляет в начала строки строку указанную в теге, например к строке "мир!" а в теге указать 
<addValueBegin mode="true">Привет </addValueBegin> то на выхоже получится "Привет мир!"

##### addValueBoth

принимает две строки на вход через запятую. Этот тег добавляет первую строчку в начало строки а вторую в конец.
Например <addValueBoth mode="true">Привет, мир!</addValueBoth> к строке ",чудесный" получится на выходе "Привет, чудесный мир!"

##### replace

отвечает за замену значения на другое значение. Если тег выключен то тег имеет вид `<replace mode="false"></replace>`
Но если вы хотите чтобы значения заменялись в этой строке то нужно включить этот тег прописав `mode="true"`
После включения этого тега вам нужно теперь добавить теги для замены, это делается следующим образом
```xml
<replace mode="true"> 
    <replaceVal>
        <value>строка_которую_надо_заменить</value>
        <toValue>строка_на_которую_надо_заменить</toValue>
    </replaceVal>
</replace>
```
блок `replaceVal` включает в себя два тега *value* и *toValue*. Тег *value* принимает строку которую нужно заменить а тег *toValue* включает в себя строку на которую нужно заменить
блоков *replaceVal* может быть сколь угодно много, например
```xml
<replace mode="true"> 
    <replaceVal>
        <value>1</value>
        <toValue>*</toValue>
    </replaceVal>
    <replaceVal>
        <value>0</value>
        <toValue> </toValue>
    </replaceVal>
    <replaceVal>
        <value>3</value>
        <toValue>**</toValue>
    </replaceVal>
</replace>
```

##### filter

Отвечает за фильтрацию поля по значению перед преобразованием значения в ячейке (если указано преобразование в тегах конфига), 
если тег включен то при истинном значении условия строка берется в выборку. У включенного тега `<filter mode="true">`
Тег имеет вид
```xml
<filter mode="true">

    <f_cropEnd mode="false"></f_cropEnd> <!-- <cropEnd mode="true/ false">value</cropEnd> -->
    <f_addValueEnd mode="false"></f_addValueEnd> <!-- <addValueEnd mode="true/ false">value</addValueEnd> -->
    <f_takeFromBegin mode="false"></f_takeFromBegin> <!-- <takeFromBegin mode="true/ false">value</takeFromBegin> -->
    <f_cropBegin mode="false"></f_cropBegin> <!-- <cropBegin mode="true/ false">value</cropBegin> -->
    <f_addValueBegin mode="false"></f_addValueBegin> <!-- <addValueBegin mode="true/ false">value,value</addValueBegin> -->
    <f_addValueBoth mode="false"></f_addValueBoth> <!-- <addValueBoth mode="true/ false">value</addValueBoth> -->
    
    <filterVal>
        <filterMode></filterMode>      <!-- != = > < <= >= -->
        <filterValue></filterValue>    <!-- value -->
    </filterVal>

    <!-- ...  -->

</filter>
```
Теги 
```xml
<f_cropEnd mode="false"></f_cropEnd> 
<f_addValueEnd mode="false"></f_addValueEnd> 
<f_takeFromBegin mode="false"></f_takeFromBegin> 
<f_cropBegin mode="false"></f_cropBegin> 
<f_addValueBegin mode="false"></f_addValueBegin> 
<f_addValueBoth mode="false"></f_addValueBoth> 
```
Изменяют значение в ячейке перед тем как начать процедуру сравнения со значением
в темге `<filterVal>` . Этот процесс изменяет значение только для процерки,
для того чтобы произвести фильтрацию по измененному значению. Но измененное
значение не идет дальше в загрузку. Фильтровать также можно и даты.
Даты в поле ``` <filterValue></filterValue> ```  в случае фильтрации дат
необходимо вводить в формате ``` %d.%m.%Y ```, например *01.01.2018*


В блоке `<filterVal>` находятся два тега отвечающие за режим фильтрации
и за значение с которым сравнивается значение в поле.

|тег|значение|
|---|---|
|<filterMode>|режим фильтрации. Значения: != = > < <= >=|
|<filterValue>|значение с которым сравнивается поле|

При режимах ` > < <= >= ` Тег `<colType>` должен быть равен `int` или `float`

##### post-filter

Отвечает за фильтрацию поля по значению после преобразованием значения в ячейке (если такое есть).
Преобразование значения ячейки происходит в тегах 
```xml
<cropEnd mode="false"></cropEnd> <!-- <cropEnd mode="true/ false">value</cropEnd> -->
<addValueEnd mode="false"></addValueEnd> <!-- <addValueEnd mode="true/ false">value</addValueEnd> -->
<takeFromBegin mode="false"></takeFromBegin> <!-- <takeFromBegin mode="true/ false">value</takeFromBegin> -->
<cropBegin mode="false"></cropBegin> <!-- <cropBegin mode="true/ false">value</cropBegin> -->
<addValueBegin mode="false"></addValueBegin> <!-- <addValueBegin mode="true/ false">value,value</addValueBegin> -->
<addValueBoth mode="false"></addValueBoth> <!-- <addValueBoth mode="true/ false">value</addValueBoth> -->
<replace mode="true">                    <!-- <replace mode="true/ false">value</replace> -->

    <replaceVal>
        <value></value>                     <!--value-->
        <toValue></toValue>                 <!--value-->
    </replaceVal>

    <!--...-->

</replace>
```
если тег включен то при истинном значении условия строка берется в выборку. У включенного тега `<post-filter mode="true">`
Тег имеет вид
```xml
<post-filter mode="true">
    <postfilterVal>
        <filterMode></filterMode>      <!-- != = > < <= >= -->
        <filterValue></filterValue>    <!-- value -->
    </postfilterVal>

    <!-- ...  -->

</post-filter>
```


##### Порядок выполнения преобразования

Если включить все теги `cropEnd addValueEnd takeFromBegin cropBegin addValueBegin addValueBoth replace` то они все обработают полученную строку
Порядок выполнения операций обработки: cropEnd, cropBegin, addValueEnd, takeFromBegin, addValueBegin, addValueBoth, replace

##### Примечание

Надо учесть, что блоков `column` в теге `importXml` может быть больше чем колонок в файле Excel, это возникает в том случае, если одна и таже колонока
идет в разные поля в базе данных. Например
```xml
<column>
    <colName>Name</colName>
    <colNameDb>Name</colNameDb>
    <colType>str</colType>
    <valueLength mode="false"></valueLength>
    <transformation mode="false"></transformation>
    <cropEnd mode="false"></cropEnd>
    <addValueEnd mode="false"></addValueEnd>
    <takeFromBegin mode="false"></takeFromBegin>
    <cropBegin mode="false"></cropBegin>
    <addValueBegin mode="false"></addValueBegin>
    <addValueBoth mode="false"></addValueBoth>
    <replace mode="false"></replace>
    <filter mode="false"></filter>
    <post-filter mode="false"></post-filter>
</column>

<column>
    <colName>Name</colName>
    <colNameDb>Name2</colNameDb>
    <colType>str</colType>
    <valueLength mode="false"></valueLength>
    <transformation mode="false"></transformation>
    <cropEnd mode="false"></cropEnd>
    <addValueEnd mode="false"></addValueEnd>
    <takeFromBegin mode="false"></takeFromBegin>
    <cropBegin mode="false"></cropBegin>
    <addValueBegin mode="false"></addValueBegin>
    <addValueBoth mode="false"></addValueBoth>
    <replace mode="false"></replace>
    <filter mode="false"></filter>
    <post-filter mode="false"></post-filter>
</column>
```

В поле `colName` в обоих случаях прописывается имя этой колонки, но в поле `colNameDb` надо указать в каждом блоке имя поля в которое пойдет это значение.
Но количество блоков column в теге `exportTable` должно быть ровно таким сколько полей в базе данных.

---
[:arrow_up:Оглавление](#Оглавление)

## Информация о структуре проекта
#### Тег exportTable

Этот блок описывает поля базы данных

```xml
<exportTable> <!-- configure receiver data base columns -->
        <path></path>            <!-- receiver data base table name [dbo].[name] -->

        <columns>

            <column>
                <name></name>                                <!-- column name in database -->
                <fromExcel></fromExcel>                  <!-- true/ false -->
                <fromDb></fromDb>                       <!-- true/ false -->
                <isAutoInc></isAutoInc>                 <!-- true/ false -->
                <isConc></isConc>                       <!-- true/ false -->
                <defaultValue mode="false"></defaultValue>   <!-- <defaultValue mode="false/tue">value</defaultValue> -->
                <colType></colType>                       <!-- str / int -->
                <isUpdateCondition></isUpdateCondition> <!-- true/ false -->
                <ifNull mode="false"></ifNull>               <!-- mode =  true/ false -->
            </column>

        <!--<column>-->
        <!--...-->
        <!--</column>-->
        <!--...-->
        <!--<column>-->
        <!--...-->
        <!--</column>-->

        </columns>
    </exportTable>
```

тег `path` включает в себя имя таблицы в базе данных

Далее идут тег блоков `columns`
Тег `columns` описывает поля в базе данных. Он содержит теги `column`
Структура тега `column` следующая 
```xml
<column>
    <name>имя_поля_в_базе_данных</name>
    <fromDb>берется_ли_поле_из_базы_данных</fromDb>
    <isAutoInc>является_ли_поле_в_базе_автоинкрементом</isAutoInc>
    <isConc>является_ли_поле_составным_из_нескольких_колонок</isConc>
    <fromExcel>берется_ли_поле_из_файла_или_дефолтное</fromExcel>
    <defaultValue mode="false\true">дефолтное_значение</defaultValue>
    <colType>str\int</colType>
    <ifNull mode="true\false">значение_если_поле_null</ifNull>
    <isUpdateCondition>участвует_ли_поле_в_запросе_update_в_условии_where</isUpdateCondition>
</column>
```

|тег|значение|
|---|---|
|name|включает в себя имя поля в базе данных|
|isAutoInc|характеризует является ли данное поле автоинкрементом в базе данных. false нет true да|
|isConc|является ли данное поле составным полем из нескольких полей.true да false нет|
|fromExcel|берется ли данное поле из файла Excel|
|defaultValue|принимает в себя строку, которую нужно вставлять когда поле не берется из файла|
|colType|описывает какого типа будут вставляться строчки. int str. Если вставляется в базу значения типа date то либо int или str это не имеет значения|
|ifNull|нужен для того, чтобы заменять поля получаемые из базы на другие значение,если они становятся налами|
|fromDb| указывает на то берется ли значение из словарной таблицы в базе. false нет true да|
|isUpdateCondition|если <isUpdateCondition>true</isUpdateCondition> то эта колонка податает в условие WHERE в апдейте и по ней будут искаться колонки для апдейта|


##### defaultValue
Например 
```xml
<fromExcel>false</fromExcel>
<defaultValue mode="true">null</defaultValue> 
```
то значит это поле будет заполняться null'ами

##### colType

По сути это значит будет ли вставляемое значение оборачиваться в кавычки или нет. 
Если поле берется не из файла и по дефолту вставляется null то нужно заполнить это поле значением int так как null в ковычках будет приниматься как строка т.е.
```xml
<fromExcel>false</fromExcel>
<defaultValue mode="true">null</defaultValue>
<colType>int</colType>
```

##### ifNull

Например

```xml
<fromExcel>true</fromExcel>
<defaultValue mode="false"></defaultValue>
<colType>str</colType>
<ifNull mode="true">null</ifNull>
```
То это значит, что полученное значение в случае null заменится на null. Тут в запросе нал будет вставляться без ковычек даже если поле строковое.

##### isUpdateCondition
работает в режиме <loadMode>update</loadMode> если <isUpdateCondition>true</isUpdateCondition> 
то эта колонка податает в условие WHERE в апдейте и по ней будут искаться колонки для апдейта
Если <ifNull mode="false"></ifNull> и одновременно <defaultValue mode="false"></defaultValue> и 
колонка берется из экселя то эта колонка будет проверяться на налы


##### isConc

Если <isConc>true</isConc> то просто в описании колонок в источнике в блоке 
importXml указываем имя этой колонки в тех колонках которые хотим соединить 
и они автоматически сверху вниз в порядке следования в конфиге соединятся

---
[:arrow_up:Оглавление](#Оглавление)

### Загрузка из файла Excel с подключением таблицы в БД 

Тег loadMode = insert и checkMode = false; dict = true

Данный режим загрузки необходим тогда, когда значения в одном или нескольких полей 
в загрузке берутся не из поля в файле Excel а из поля в базе данных.

В данном режиме загрузки конфигурация файла настйроки загрузки остается той же,
только теперь тег `<dict></dict>` принимает значение `<dict>true</dict>`

Файл конфигурации принимает следующий вид:

```xml
<?xml version="1.0"?>

<main>
    <dbtype></dbtype> mssql/mysql
    <dbHost></dbHost> имя хоста базы
    <dbUser></dbUser> имя пользователя базы
    <dbPass></dbPass> пароль от пользователя
    <dbBase></dbBase> имя базы
    <dbPort></dbPort> порт
    <loadMode>insert</loadMode> <!-- insert / update -->
    <dict>true</dict> <!-- true/ false -->
    <checkMode>false</checkMode> <!-- true/false -->
   

    <importXml>                в этом блоке лежат блоки описания источников для полей базы
        <path></path>          имя файла excel из которого будет идти загрузка
        <sheetNumber>1</sheetNumber>   номер страницы на которой нужно открыть excel, нумерация с 1

        <columns>              
        	{тут лежит список колонок источников для базы}
        </columns>
        
        
        <linkedColumns mode="false"></linkedColumns>
    
        <withDict mode="true"> <!-- true/ false" -->
            <tables>
                {тут может быть несоклько тегов <table>}
                <table>
                    <dictTableName></dictTableName> <!-- table name in data base -->
                    <indxDbColumn>indx_1</indxDbColumn> <!-- index column name in receiver -->
                    <indxColumnDic>indx</indxColumnDic> <!-- index column name in dictionary -->
                        <columns>
                            <column>
                                <colName></colName> <!-- column name in excel -->
                                <colNameDb></colNameDb> <!-- colum name in db -->
                                <colType></colType> <!-- str / int / float / date-->
                                <cropEnd mode="false"></cropEnd> <!-- <cropEnd mode="true/ false">value</cropEnd> -->
                                <addValueEnd mode="false"></addValueEnd> <!-- <addValueEnd mode="true/ false">value</addValueEnd> -->
                                <takeFromBegin mode="false"></takeFromBegin> <!-- <takeFromBegin mode="true/ false">value</takeFromBegin> -->
                                <cropBegin mode="false"></cropBegin> <!-- <cropBegin mode="true/ false">value</cropBegin> -->
                                <addValueBegin mode="false"></addValueBegin> <!-- <addValueBegin mode="true/ false">value</addValueBegin> -->
                                <addValueBoth mode="false"></addValueBoth> <!-- <addValueBoth mode="true/ false">value</addValueBoth> -->
                                <replace mode="false"></replace>
                            </column>
                        </columns>
                </table>
            </tables>
        </withDict>
        
        
    </importXml>
    

    <exportTable>              в этом блоке лежат блоки описания полей базы данных
        <path>[dbo].[имя_таблицы]</path>   имя таблицы в базе
        <columns>
        	{тут лежит список колонок в базе данных}
        </columns>
    </exportTable>
</main>
```


---
[:arrow_up:Оглавление](#Оглавление)

#### Тег withDict

он нужен для описания таблицы в базе данных из которой будут браться значения для поля который будет
вставляться в базу данных

```xml
<withDict mode="true"> <!-- true/ false" -->

            <tables>
                <table>
                    <dictTableName></dictTableName> <!-- table name in data base -->
                    <indxDbColumn>indx_1</indxDbColumn> <!-- index column name in receiver -->
                    <indxColumnDic>indx</indxColumnDic> <!-- index column name in dictionary -->

                        <columns>
                            <column>
                                <colName></colName> <!-- column name in excel -->
                                <colNameDb></colNameDb> <!-- colum name in db -->
                                <colType></colType> <!-- str / int / float / date -->
                                <cropEnd mode="false"></cropEnd> <!-- <cropEnd mode="true/ false">value</cropEnd> -->
                                <addValueEnd mode="false"></addValueEnd> <!-- <addValueEnd mode="true/ false">value</addValueEnd> -->
                                <takeFromBegin mode="false"></takeFromBegin> <!-- <takeFromBegin mode="true/ false">value</takeFromBegin> -->
                                <cropBegin mode="false"></cropBegin> <!-- <cropBegin mode="true/ false">value</cropBegin> -->
                                <addValueBegin mode="false"></addValueBegin> <!-- <addValueBegin mode="true/ false">value</addValueBegin> -->
                                <addValueBoth mode="false"></addValueBoth> <!-- <addValueBoth mode="true/ false">value</addValueBoth> -->
                                <replace mode="false">                    <!-- <replace mode="true/ false">value</replace> -->

                                <replaceVal>
                                    <value></value>                     <!--value-->
                                    <toValue></toValue>                 <!--value-->
                                </replaceVal>

                                <!--...-->

                                </replace>
                            </column>

                        <!--<column>-->
                        <!--...-->
                        <!--</column>-->
                        <!--...-->
                        <!--<column>-->
                        <!--...-->
                        <!--</column>-->

                        </columns>
                </table>

            <!--<table></table>-->
            <!---->
            <!--...-->
            <!---->
            <!--<table></table>-->


            </tables>
        </withDict>
```

Он включает в себя тег `tables` в котором хранится список таблиц заключенные в теги `table`
В теге table содержатся следующие теги

|тег|значение|
|---|---|
|dictTableName|имя таблицы словарной из которой берем индекс|
|indxDbColumn|имя колонки с индексом в целевой таблице куда кладем индекс|
|indxColumnDic|имя колонки с индексом в словарной таблице откуда берем индекс|

Дальше идут теги с колонками тут все также как в источнике, указываем имя колонки в экселе имя колонки в словарной таблице куда была
загружена эта колонка а также операции которые нужно сделать с колонкой из экселя

#### Особенности данного режима

В данном режиме надо учесть, то, что описывая конфигурацию полей в базе данных, 
у поля, которое берется из таблицы в базе данных, надо указать то что поле берется
из базы данных, например

```xml
<column>
    <name>Name</name>                                
    <fromExcel>false</fromExcel>     < тут указать то что не берется              
    <fromDb>true</fromDb>            < тут указать то что берется           
    <isAutoInc>false</isAutoInc>                 
    <isConc>false</isConc>                       
    <defaultValue mode="false"></defaultValue>   
    <colType>str</colType>                       
    <isUpdateCondition>false</isUpdateCondition> 
    <ifNull mode="false"></ifNull>               
</column>
```

---
[:arrow_up:Оглавление](#Оглавление)


### Режим сравнения двух файлов Excel

Тег loadMode = insert и checkMode = true; dict = false
В данном режиме загрузчик превращается в систему для сравнения файлов
Поэтому часть негов указывать не обязательно

```xml
<?xml version="1.0"?>

<main>
    <dbtype></dbtype> mssql/mysql
    <dbHost></dbHost> имя хоста базы
    <dbUser></dbUser> имя пользователя базы
    <dbPass></dbPass> пароль от пользователя
    <dbBase></dbBase> имя базы
    <dbPort></dbPort> порт
    <loadMode>insert</loadMode> <!-- insert / update -->
    <dict>false</dict> <!-- true/ false -->
    <checkMode>true</checkMode> <!-- true/false -->
   

    <importXml>                в этом блоке лежат блоки описания источников для полей базы
        <path></path>          имя файла excel из которого будет идти загрузка
        <sheetNumber>1</sheetNumber>   номер страницы на которой нужно открыть excel, нумерация с 1

        <columns>              
        	{тут лежит список колонок источников для базы}
        </columns>
        
        <linkedColumns mode="true"> <!-- <linkedColumns mode="true / false"> -->
        <!--only for check mode-->
            <pathToLinkFile></pathToLinkFile> <!-- excel file name.xlsx -->
            <linkedFileSheetNumber></linkedFileSheetNumber> <!-- List number in excel [1... ] -->
            <both></both>                                   <!-- true / false -->

            <column>
                <linkedColName></linkedColName> <!-- column name in excel file to compare -->
                <colNameInSource></colNameInSource> <!-- column name in source excel -->
            </column>

            {тут список колонок для сравнения}

        </linkedColumns>
        
    </importXml>
</main>
```

---
[:arrow_up:Оглавление](#Оглавление)
## Информация о структуре проекта

### Тег linkedColumns

этот тег нужен для режима сравения двух файлов 
Он работает только в режиме `<checkMode>true</checkMode>`. В режиме загрузки *insert* ставим `<checkMode>true</checkMode>` а `<linkedColumns mode="true">`

```xml
<linkedColumns mode="true"> <!-- <linkedColumns mode="true / false"> -->
        <!--only for check mode-->
            <pathToLinkFile></pathToLinkFile> <!-- excel file name.xlsx -->
            <linkedFileSheetNumber></linkedFileSheetNumber> <!-- List number in excel [1... ] -->
            <both></both>                                   <!-- true / false -->

            <column>
                <linkedColName></linkedColName> <!-- column name in excel file to compare -->
                <colNameInSource></colNameInSource> <!-- column name in source excel -->
            </column>

        <!--<column>-->
            <!--...-->
        <!--</column>-->
        <!--...-->
        <!--<column>-->
            <!--...-->
        <!--</column>-->

</linkedColumns>
```

в этом теге содержатся теги

|тег|значение|
|---|---|
|pathToLinkFile|имя сравниваемого экселя. положить надо тудаже где и все эксели|
|linkedFileSheetNumber|номер страницы на которой открыть сравниваемый эксель. нумерация с 1|


дальше идет перечисление колонок для сравнения в теге `column`

|тег|значение|
|---|---|
|linkedColName|имя колонки в сравниаемом экселе|
|colNameInSource|имя колонки в источнике|
|both|true если надо сравнивать источник со словарем и обратно словарь с источником. false если только источник со словарем|

если не надо сравнивать и checkMode == false то можно просто оставить тег пустым <linkedColumns mode="false"></linkedColumns>

---
[:arrow_up:Оглавление](#Оглавление)

### Режим обновления записей в БД
Тег loadMode = update и checkMode = false; dict = false
Конфигурация тегов в данном режиме имеет следующий вид

```xml
<?xml version="1.0"?>

<main>
    <dbtype></dbtype> mssql/mysql
    <dbHost></dbHost> имя хоста базы
    <dbUser></dbUser> имя пользователя базы
    <dbPass></dbPass> пароль от пользователя
    <dbBase></dbBase> имя базы
    <dbPort></dbPort> порт
    <loadMode>update</loadMode> <!-- insert / update -->
    <dict>false</dict> <!-- true/ false -->
    <checkMode>false</checkMode> <!-- true/false -->
   

    <importXml>                в этом блоке лежат блоки описания источников для полей базы
        <path></path>          имя файла excel из которого будет идти загрузка
        <sheetNumber>1</sheetNumber>   номер страницы на которой нужно открыть excel, нумерация с 1

        <columns>              
        	{тут лежит список колонок источников для базы}
        </columns>
        
        <linkedColumns mode="false"></linkedColumns>
        <withDict mode="false"></withDict>
        
    </importXml>
    
    
    
    
    <exportTable>              в этом блоке лежат блоки описания полей базы данных
        <path>[dbo].[имя_таблицы]</path>   имя таблицы в базе
        <columns>
        	{тут лежит список колонок в базе данных}
        </columns>
    </exportTable>
</main>
```

Здесь изменения касаются только конфигурации описания полей в базе данных
Необходимо указать хотя бы у одного поля то что оно используется для формирования запроса
Например

```xml
<column>
    <name>Name</name>                                
    <fromExcel>true</fromExcel>                  
    <fromDb>false</fromDb>                       
    <isAutoInc>false</isAutoInc>                 
    <isConc>false</isConc>                       
    <defaultValue mode="false"></defaultValue>   
    <colType>str</colType>                       
    <isUpdateCondition>true</isUpdateCondition>   < здесь указывается поле true 
    <ifNull mode="false"></ifNull>               
</column>
``` 


---
[:arrow_up:Оглавление](#Оглавление)


## Пример загрузки

Допустим нам нужно загрузить данные в таблицу `central` со следующей конфигурацией:

|Поле|Тип|ключ|
|---|---|---|
|indx_1|int|внешний ключ к таблице dic_1|
|indx_2|int|внешний ключ к таблице dic_2|
|col_1|varchar|-|
|col_2|varchar|-|
|col_3|varchar|-|

Но так как в этой таблице имеется два поля `indx_1 indx_2` которые ссылаются
на две другие таблицы, то нужно предварительно прогрузить значения в эти две таблицы

Таблицы dic_1 и dic_2 имеют следующие конфигуации

```dic_1```

|Поле|Тип|ключ|
|---|---|---|
|col_1|varchar|-|
|col_2|varchar|-|
|col_3|varchar|-|
|indx|int|первичный ключ, автоинкремент|

```dic_2```

|Поле|Тип|ключ|
|---|---|---|
|col_1|varchar|-|
|col_2|varchar|-|
|indx|int|первичный ключ, автоинкремент|

А также источник данных excel файл который имеет следующие поля

|Поле|Тип|
|---|---|
|dict_1_1|строка|
|dict_1_2|строка|
|dict_1_3|дата|
|dict_2_1|строка|
|dict_2_2|строка|
|col_1|строка|
|col_2|строка|
|col_3|строка|

Для загрузки данных необходимо положить эксель файл `source.xlsx` в корень проекта в папку `Source`.

Затем в папке проекта необходимо создать три файла конфигурации (два для
загрузки двух таблиц и третью для загрузки целевой таблицы)

Первый файл назовем `dic_1.xml`. Его содержимое

```xml
<?xml version="1.0"?>

<main>
    <dbtype>mysql</dbtype> 
    <dbHost>localhost</dbHost> 
    <dbUser>user</dbUser> 
    <dbPass>password</dbPass> 
    <dbBase>dbbase</dbBase> 
    <dbPort>3306</dbPort> 
    <loadMode>insert</loadMode> 
    <dict>false</dict> 
    <checkMode>false</checkMode> 

    <importXml> 
        <path>source.xlsx</path> 
        <sheetNumber>1</sheetNumber> 

        <columns>

            <column>
                <colName>dict_1_1</colName> 
                <colNameDb>col_1</colNameDb> 
                <colType>str</colType> 
                <isPK>false</isPK> 
                <cropEnd mode="false"></cropEnd> 
                <addValueEnd mode="false"></addValueEnd> 
                <takeFromBegin mode="false"></takeFromBegin> 
                <cropBegin mode="false"></cropBegin> 
                <addValueBegin mode="false"></addValueBegin> 
                <addValueBoth mode="false"></addValueBoth> 
                <replace mode="false"></replace>
                <filter mode="false"></filter>
                <post-filter mode="false"></post-filter>
            </column>

            <column>
                <colName>dict_1_2</colName> 
                <colNameDb>col_2</colNameDb> 
                <colType>str</colType> 
                <isPK>false</isPK> 
                <cropEnd mode="false"></cropEnd> 
                <addValueEnd mode="false"></addValueEnd> 
                <takeFromBegin mode="false"></takeFromBegin> 
                <cropBegin mode="false"></cropBegin> 
                <addValueBegin mode="false"></addValueBegin> 
                <addValueBoth mode="false"></addValueBoth> 
                <replace mode="false"></replace>
                <filter mode="false"></filter>
                <post-filter mode="false"></post-filter>
            </column>

            <column>
                <colName>dict_1_3</colName> 
                <colNameDb>col_3</colNameDb> 
                <colType>date</colType> 
                <isPK>false</isPK> 
                <cropEnd mode="false"></cropEnd> 
                <addValueEnd mode="false"></addValueEnd> 
                <takeFromBegin mode="false"></takeFromBegin> 
                <cropBegin mode="false"></cropBegin> 
                <addValueBegin mode="false"></addValueBegin> 
                <addValueBoth mode="false"></addValueBoth> 
                <replace mode="false"></replace>
                <filter mode="false"></filter>
                <post-filter mode="false"></post-filter>
            </column>

        </columns>


        <linkedColumns mode="false"></linkedColumns>

        <withDict mode="false"></withDict>

    </importXml>

    <exportTable> 
        <path>dic_1</path>            

        <columns>

            <column>
                <name>col_1</name>                                
                <fromExcel>true</fromExcel>                  
                <fromDb>false</fromDb>                       
                <isAutoInc>false</isAutoInc>                 
                <isConc>false</isConc>                       
                <defaultValue mode="false"></defaultValue>   
                <colType>str</colType>                       
                <isUpdateCondition>false</isUpdateCondition> 
                <ifNull mode="false"></ifNull>               
            </column>

            <column>
                <name>col_2</name>                                
                <fromExcel>true</fromExcel>                  
                <fromDb>false</fromDb>                       
                <isAutoInc>false</isAutoInc>                 
                <isConc>false</isConc>                       
                <defaultValue mode="false"></defaultValue>   
                <colType>str</colType>                       
                <isUpdateCondition>false</isUpdateCondition> 
                <ifNull mode="false"></ifNull>                 
            </column>

            <column>
                <name>col_3</name>                                
                <fromExcel>true</fromExcel>                  
                <fromDb>false</fromDb>                       
                <isAutoInc>false</isAutoInc>                 
                <isConc>false</isConc>                       
                <defaultValue mode="false"></defaultValue>   
                <colType>str</colType>                       
                <isUpdateCondition>false</isUpdateCondition> 
                <ifNull mode="false"></ifNull>                 
            </column>

            <column>
                <name>indx</name>                                
                <fromExcel>false</fromExcel>                 
                <fromDb>false</fromDb>                     
                <isAutoInc>true</isAutoInc>                 
                <isConc>false</isConc>                    
                <defaultValue mode="false"></defaultValue>   
                <colType>str</colType>                   
                <isUpdateCondition>false</isUpdateCondition> 
                <ifNull mode="false"></ifNull>                 
            </column>

        </columns>
    </exportTable>
</main>

```

Второй файл назовем `dic_2.xml`. Его содержимое

```xml
<?xml version="1.0"?>

<main>
    <dbtype>mysql</dbtype> 
    <dbHost>localhost</dbHost> 
    <dbUser>user</dbUser> 
    <dbPass>password</dbPass> 
    <dbBase>dbbase</dbBase> 
    <dbPort>3306</dbPort> 
    <loadMode>insert</loadMode> 
    <dict>false</dict> 
    <checkMode>false</checkMode> 

    <importXml> 
        <path>source.xlsx</path>  
        <sheetNumber>1</sheetNumber>  

        <columns>

            <column>
                <colName>dict_2_1</colName> 
                <colNameDb>col_1</colNameDb>  
                <colType>str</colType>  
                <isPK>false</isPK>  
                <cropEnd mode="false"></cropEnd> 
                <addValueEnd mode="false"></addValueEnd>  
                <takeFromBegin mode="false"></takeFromBegin>  
                <cropBegin mode="false"></cropBegin>  
                <addValueBegin mode="false"></addValueBegin>  
                <addValueBoth mode="false"></addValueBoth> 
                <replace mode="false"></replace>
                <filter mode="false"></filter>
                <post-filter mode="false"></post-filter>
            </column>

            <column>
                <colName>dict_2_2</colName>  
                <colNameDb>col_2</colNameDb>  
                <colType>str</colType>  
                <isPK>false</isPK>  
                <cropEnd mode="false"></cropEnd> 
                <addValueEnd mode="false"></addValueEnd>  
                <takeFromBegin mode="false"></takeFromBegin>  
                <cropBegin mode="false"></cropBegin>  
                <addValueBegin mode="false"></addValueBegin>  
                <addValueBoth mode="false"></addValueBoth>  
                <replace mode="false"></replace>
                <filter mode="false"></filter>
                <post-filter mode="false"></post-filter>
            </column>

        </columns>


        <linkedColumns mode="false"></linkedColumns>

        <withDict mode="false"></withDict>

    </importXml>

    <exportTable>  
        <path>dic_2</path>    

        <columns>

            <column>
                <name>col_1</name>                       
                <fromExcel>true</fromExcel>           
                <fromDb>false</fromDb>                 
                <isAutoInc>false</isAutoInc>             
                <isConc>false</isConc>                
                <defaultValue mode="false"></defaultValue>    
                <colType>str</colType>        
                <isUpdateCondition>false</isUpdateCondition>  
                <ifNull mode="false"></ifNull>             
            </column>

            <column>
                <name>col_2</name>                         
                <fromExcel>true</fromExcel>              
                <fromDb>false</fromDb>                 
                <isAutoInc>false</isAutoInc>              
                <isConc>false</isConc>              
                <defaultValue mode="false"></defaultValue>    
                <colType>str</colType>                    
                <isUpdateCondition>false</isUpdateCondition>  
                <ifNull mode="false"></ifNull>            
            </column>

            <column>
                <name>indx</name>                           
                <fromExcel>false</fromExcel>             
                <fromDb>false</fromDb>                  
                <isAutoInc>true</isAutoInc>       
                <isConc>false</isConc>                   
                <defaultValue mode="false"></defaultValue>   
                <colType>str</colType>           
                <isUpdateCondition>false</isUpdateCondition>  
                <ifNull mode="false"></ifNull>               
            </column>

        </columns>
    </exportTable>
</main>

```

Конфигурационный файл основной загрузки назовем ```main.xml``` 

```xml
<?xml version="1.0"?>

<main>
    <dbtype>mysql</dbtype> 
    <dbHost>localhost</dbHost> 
    <dbUser>user</dbUser> 
    <dbPass>password</dbPass> 
    <dbBase>dbbase</dbBase> 
    <dbPort>3306</dbPort> 
    <loadMode>insert</loadMode> 
    <dict>true</dict> 
    <checkMode>false</checkMode> 

    <importXml> 
        <path>source.xlsx</path>  
        <sheetNumber>1</sheetNumber>  

        <columns>

            <column>
                <colName>col_1</colName>  
                <colNameDb>col_1</colNameDb> 
                <colType>str</colType>  
                <isPK>false</isPK>  
                <cropEnd mode="false"></cropEnd>  
                <addValueEnd mode="false"></addValueEnd>  
                <takeFromBegin mode="false"></takeFromBegin>  
                <cropBegin mode="false"></cropBegin>  
                <addValueBegin mode="false"></addValueBegin>  
                <addValueBoth mode="false"></addValueBoth>  
                <replace mode="false"></replace>
                <filter mode="false"></filter>
                <post-filter mode="false"></post-filter>
            </column>

            <column>
                <colName>col_2</colName> 
                <colNameDb>col_2</colNameDb>  
                <colType>str</colType>  
                <isPK>false</isPK> 
                <cropEnd mode="false"></cropEnd>  
                <addValueEnd mode="false"></addValueEnd> 
                <takeFromBegin mode="false"></takeFromBegin>  
                <cropBegin mode="false"></cropBegin> 
                <addValueBegin mode="false"></addValueBegin> 
                <addValueBoth mode="false"></addValueBoth>  
                <replace mode="false"></replace>
                <filter mode="false"></filter>
                <post-filter mode="false"></post-filter>
            </column>

            <column>
                <colName>col_3</colName>  
                <colNameDb>col_3</colNameDb>  
                <colType>str</colType>  
                <isPK>false</isPK>  
                <cropEnd mode="false"></cropEnd>  
                <addValueEnd mode="false"></addValueEnd>  
                <takeFromBegin mode="false"></takeFromBegin>  
                <cropBegin mode="false"></cropBegin> 
                <addValueBegin mode="false"></addValueBegin>  
                <addValueBoth mode="false"></addValueBoth> 
                <replace mode="false"></replace>
                <filter mode="false"></filter>
                <post-filter mode="false"></post-filter>
            </column>


        </columns>


        <linkedColumns mode="false"></linkedColumns>

        <withDict mode="true">  

            <tables>

                <table>
                    <dictTableName>dic_1</dictTableName>  
                    <indxDbColumn>indx_1</indxDbColumn>  
                    <indxColumnDic>indx</indxColumnDic> 

                        <columns>

                            <column>
                                <colName>dict_1_1</colName>  
                                <colNameDb>col_1</colNameDb>  
                                <colType>str</colType>  
                                <cropEnd mode="false"></cropEnd>  
                                <addValueEnd mode="false"></addValueEnd> 
                                <takeFromBegin mode="false"></takeFromBegin>  
                                <cropBegin mode="false"></cropBegin>  
                                <addValueBegin mode="false"></addValueBegin> 
                                <addValueBoth mode="false"></addValueBoth>  
                                <replace mode="false"></replace>
                            </column>


                            <column>
                                <colName>dict_1_2</colName>  
                                <colNameDb>col_2</colNameDb>  
                                <colType>str</colType>  
                                <cropEnd mode="false"></cropEnd> 
                                <addValueEnd mode="false"></addValueEnd>  
                                <takeFromBegin mode="false"></takeFromBegin>  
                                <cropBegin mode="false"></cropBegin>  
                                <addValueBegin mode="false"></addValueBegin>  
                                <addValueBoth mode="false"></addValueBoth>  
                                <replace mode="false"></replace>
                            </column>


                            <column>
                                <colName>dict_1_3</colName>  
                                <colNameDb>col_3</colNameDb>  
                                <colType>date</colType>  
                                <cropEnd mode="false"></cropEnd> 
                                <addValueEnd mode="false"></addValueEnd>  
                                <takeFromBegin mode="false"></takeFromBegin>  
                                <cropBegin mode="false"></cropBegin> 
                                <addValueBegin mode="false"></addValueBegin>  
                                <addValueBoth mode="false"></addValueBoth> 
                                <replace mode="false"></replace>
                            </column>
                        </columns>
                </table>

                <table>
                    <dictTableName>dic_2</dictTableName>  
                    <indxDbColumn>indx_2</indxDbColumn>  
                    <indxColumnDic>indx</indxColumnDic>  

                        <columns>

                            <column>
                                <colName>dict_2_1</colName>  
                                <colNameDb>col_1</colNameDb> 
                                <colType>str</colType>  
                                <cropEnd mode="false"></cropEnd>  
                                <addValueEnd mode="false"></addValueEnd>  
                                <takeFromBegin mode="false"></takeFromBegin>  
                                <cropBegin mode="false"></cropBegin>  
                                <addValueBegin mode="false"></addValueBegin>  
                                <addValueBoth mode="false"></addValueBoth>  
                                <replace mode="false"></replace>
                            </column>

                            <column>
                                <colName>dict_2_2</colName>  
                                <colNameDb>col_2</colNameDb>  
                                <colType>str</colType>  
                                <cropEnd mode="false"></cropEnd> 
                                <addValueEnd mode="false"></addValueEnd>  
                                <takeFromBegin mode="false"></takeFromBegin>  
                                <cropBegin mode="false"></cropBegin>  
                                <addValueBegin mode="false"></addValueBegin>  
                                <addValueBoth mode="false"></addValueBoth>  
                                <replace mode="false"></replace>
                            </column>

                        </columns>
                </table>

            </tables>
        </withDict>

    </importXml>

    <exportTable>  
        <path>central</path>          

        <columns>

            <column>
                <name>col_1</name>                       
                <fromExcel>true</fromExcel>             
                <fromDb>false</fromDb>                 
                <isAutoInc>false</isAutoInc>            
                <isConc>false</isConc>                     
                <defaultValue mode="false"></defaultValue>   
                <colType>str</colType>                    
                <isUpdateCondition>false</isUpdateCondition>  
                <ifNull mode="false"></ifNull>           
            </column>

            <column>
                <name>col_2</name>                            
                <fromExcel>true</fromExcel>                
                <fromDb>false</fromDb>                     
                <isAutoInc>false</isAutoInc>                 
                <isConc>false</isConc>                    
                <defaultValue mode="false"></defaultValue>   
                <colType>str</colType>                     
                <isUpdateCondition>false</isUpdateCondition> 
                <ifNull mode="false"></ifNull>              
            </column>

            <column>
                <name>col_3</name>                           
                <fromExcel>true</fromExcel>             
                <fromDb>false</fromDb>                  
                <isAutoInc>false</isAutoInc>            
                <isConc>false</isConc>                     
                <defaultValue mode="false"></defaultValue>  
                <colType>str</colType>                       
                <isUpdateCondition>false</isUpdateCondition>  
                <ifNull mode="false"></ifNull>                
            </column>

            <column>
                <name>indx_1</name>                          
                <fromExcel>false</fromExcel>              
                <fromDb>true</fromDb>                    
                <isAutoInc>false</isAutoInc>               
                <isConc>false</isConc>                    
                <defaultValue mode="false"></defaultValue>  
                <colType>int</colType>                    
                <isUpdateCondition>false</isUpdateCondition>  
                <ifNull mode="false"></ifNull>               
            </column>

            <column>
                <name>indx_2</name>                            
                <fromExcel>false</fromExcel>                 
                <fromDb>true</fromDb>                 
                <isAutoInc>false</isAutoInc>           
                <isConc>false</isConc>                    
                <defaultValue mode="false"></defaultValue>  
                <colType>int</colType>                     
                <isUpdateCondition>false</isUpdateCondition>  
                <ifNull mode="false"></ifNull>               
            </column>

        </columns>
    </exportTable>
</main>

```

Для запуска загруки необходимо открыть консоль из корневой директории ```Core```
и написать в консоли следующую команду 

```
python Main_excel parser.py --test_mode true --config dic_1.xml dic_2.xml main.xml
```

Дання команда запустит все три конфигурации в тестовом режиме. Зайдя в корневую
директорию `log` и найдя папку с данной загрузкой можно открыть файл `debug.txt`
и убедиться в том, что все команды вставки сформировались корректно

Далее выполним загрузку в базу данных следующей командой 

```
python Main_excel parser.py --test_mode false --config dic_1.xml dic_2.xml main.xml
```

Из листинга логов мы увидим то, что загрузка прошла успешно


```
2019-09-12 18:36:58,185 - ETL - INFO - Starts executing... dic_1.xml
2019-09-12 18:36:58,217 - ETL - INFO - Success open excel file: <source.xlsx> on page name: <Sheet1>, list number: <1>
2019-09-12 18:36:58,281 - ETL - INFO - Success connection to host: <localhost>, port: <3306>, database name: <dbbase>
2019-09-12 18:36:58,281 - ETL - INFO - Begin validating files...
2019-09-12 18:36:58,287 - ETL - INFO - Validate success...
2019-09-12 18:36:58,287 - ETL - INFO - Loading in db begin...
2019-09-12 18:36:58,287 - ETL - INFO - Test mode: <false>
2019-09-12 18:36:58,288 - ETL - INFO - Rows readed: 0%
2019-09-12 18:36:58,294 - ETL - INFO - Rows readed: 25%
2019-09-12 18:36:58,297 - ETL - INFO - Rows readed: 50%
2019-09-12 18:36:58,301 - ETL - INFO - Rows readed: 75%
2019-09-12 18:36:58,303 - ETL - INFO - Rows readed: 100%
2019-09-12 18:36:58,304 - ETL - INFO - Inserted: <9>; Rows lost: <0>
2019-09-12 18:36:58,304 - ETL - INFO - Log files created in: </Designer_Etl/Core/../log/2019_09_12_18_36_58_['dic_1.xml', 'dic_2.xml', 'main.xml']>
2019-09-12 18:36:58,304 - ETL - INFO - Ends executing... successfully completed <dic_1.xml>
---
2019-09-12 18:36:58,305 - ETL - INFO - Starts executing... dic_2.xml
2019-09-12 18:36:58,312 - ETL - INFO - Success open excel file: <source.xlsx> on page name: <Sheet1>, list number: <1>
2019-09-12 18:36:58,312 - ETL - INFO - Success connection to host: <localhost>, port: <3306>, database name: <dbbase>
2019-09-12 18:36:58,312 - ETL - INFO - Begin validating files...
2019-09-12 18:36:58,313 - ETL - INFO - Validate success...
2019-09-12 18:36:58,314 - ETL - INFO - Loading in db begin...
2019-09-12 18:36:58,314 - ETL - INFO - Test mode: <false>
2019-09-12 18:36:58,314 - ETL - INFO - Rows readed: 0%
2019-09-12 18:36:58,320 - ETL - INFO - Rows readed: 25%
2019-09-12 18:36:58,322 - ETL - INFO - Rows readed: 50%
2019-09-12 18:36:58,326 - ETL - INFO - Rows readed: 75%
2019-09-12 18:36:58,327 - ETL - INFO - Rows readed: 100%
2019-09-12 18:36:58,328 - ETL - INFO - Inserted: <9>; Rows lost: <0>
2019-09-12 18:36:58,328 - ETL - INFO - Log files created in: </Designer_Etl/Core/../log/2019_09_12_18_36_58_['dic_1.xml', 'dic_2.xml', 'main.xml']>
2019-09-12 18:36:58,328 - ETL - INFO - Ends executing... successfully completed <dic_2.xml>
---
2019-09-12 18:36:58,329 - ETL - INFO - Starts executing... main.xml
2019-09-12 18:36:58,336 - ETL - INFO - Success open excel file: <source.xlsx> on page name: <Sheet1>, list number: <1>
2019-09-12 18:36:58,336 - ETL - INFO - Success connection to host: <localhost>, port: <3306>, database name: <dbbase>
2019-09-12 18:36:58,336 - ETL - INFO - Begin validating files...
2019-09-12 18:36:58,337 - ETL - INFO - Validate success...
2019-09-12 18:36:58,338 - ETL - INFO - Loading in db begin...
2019-09-12 18:36:58,338 - ETL - INFO - Test mode: <false>
2019-09-12 18:36:58,354 - ETL - INFO - Rows readed: 0%
2019-09-12 18:36:58,377 - ETL - INFO - Rows readed: 25%
2019-09-12 18:36:58,392 - ETL - INFO - Rows readed: 50%
2019-09-12 18:36:58,415 - ETL - INFO - Rows readed: 75%
2019-09-12 18:36:58,424 - ETL - INFO - Rows readed: 100%
2019-09-12 18:36:58,425 - ETL - INFO - Inserted: <9>; Rows lost: <0>
2019-09-12 18:36:58,425 - ETL - INFO - Log files created in: </Designer_Etl/Core/../log/2019_09_12_18_36_58_['dic_1.xml', 'dic_2.xml', 'main.xml']>
2019-09-12 18:36:58,425 - ETL - INFO - Ends executing... successfully completed <main.xml>
---
2019-09-12 18:36:58,430 - ETL - INFO - Connection to DB closed
```


---
[:arrow_up:Оглавление](#Оглавление)














