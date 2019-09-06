# Designer_Etl
## Описание приложения

Данное приложение разработано для осуществления загрузки из файла формата
Excel в базы данных MySQL и Microsoft SQL. Для работы приложения 
необходим установленный Python 3.7 или выше. Этим приложением можно быстро
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
7. []()
8. [Режимы работы]()
9. [Описание ошибок]()

## Установка тебуемых пакетов

Для установки требуемых пакетов выполните в консоли следующие команды: 
```
pip install pandas
pip install pymssql
pip install mysql-connector-python
pip install xlrd
```

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

После информации о ошибках при загрузке идет строка `Inserted: <КОЛИЧЕСТВО ВСТАВЛЕННЫХ СТРОК>; Rows lost: <КОЛИЧЕСТВО СТРОК НЕ ВСТАВЛЕННЫХ>`

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
```
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
                <colType></colType> <!-- str / int / float -->
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
                                <colType></colType> <!-- str / int / float -->
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
Открыть консоль и зайти в папку с проектом в директорию *Core*, проще всего 
сделать это следующим образом: открываете в проводнике папку с проектом, заходите
в директорию *Core* и выделив и удалив строку вверху где прописан путь до папки
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
| --confog конфигуратор.xml | Загрузка с выполением одного файла конфигурации |
| --confog конфигуратор1.xml конфигуратор2.xml и т.д. | Загрузка с выполением нескольких файлов конфигурации |


---
[:arrow_up:Оглавление](#Оглавление)

## Настройка файла конфигурации

### Описание

В папке сonfig лежит файл CONFIG.xml это файл конфигурации который служит для понимания структуры конфигурации. В нем
лежит структура файла конфигурации в общем виде

Файл конфигуратор представляет собой файл для настроек загрузки из файла excel в базу данных
файл имеет слудующую структуру:
каждое значение заключено в теги вида  
```
<имя_ега>значение</имя_ега>
```
также у некоторых тегов есть свойства вида 
```
<имя_ега mode="значение свойства">значение</имя_ега>
```
значение свойства бывают либо `false` либо `true`
если хотите указать число то пишите число в тег, если даже строку то пишите просто строку без ковычек то есть  

~~<имя_ега>'значение'</имя_ега>~~ 

о предназначении свойств будет рассказано далее

конфигратор имеет следующее древовидное значение:

## Теги подключения к базе данных и режимы загрузки
```
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


##  Конфигурации режимов работы загрузчика

Далее рассмотрим два варианта работы загрузчика. Они настраиваются в теге 
```<loadMode></loadMode>```

Рассмотрим сначала вариант

`<loadMode>insert</loadMode>`

При этом условимся то что

```
<checkMode>false</checkMode> 
<dict>false</dict>
```

Данная условность говорит о том, что загрузка происходит в БД напрямую из файла
Описанные ниже теги всегда присутсвуют в файле конфигурации независимо от конфигурации базы и файла источника данных для данного вида загрузки

```
<?xml version="1.0"?>

<main>
    <dbtype></dbtype> mssql/mysql
    <dbHost></dbHost> имя хоста базы
    <dbUser></dbUser> имя пользователя базы
    <dbPass></dbPass> пароль от пользователя
    <dbBase></dbBase> имя базы
    <dbPort></dbPort> порт
    <loadMode></loadMode> <!-- insert / update -->
    <dict></dict> <!-- true/ false -->
    <checkMode></checkMode> <!-- true/false -->
   

    <importXml>                в этом блоке лежат блоки описания источников для полей базы
        <path></path>          имя файла excel из которого будет идти загрузка
        <sheetNumber>1</sheetNumber>   номер страницы на которой нужно открыть excel, нумерация с 1

        <columns>              
        	{тут лежит список колонок источников для базы}
        </columns>
    </importXml>
    
    <linkedColumns mode="false"></linkedColumns>
    <withDict mode="false"></withDict>
    
    
    <exportTable>              в этом блоке лежат блоки описания полей базы данных
        <path>[dbo].[имя_таблицы]</path>   имя таблицы в базе
        <columns>
        	{тут лежит список колонок в базе данных}
        </columns>
    </exportTable>
</main>
```

### Блок importXml
Смысл этого блока в том, что он сожержит данные об источнике данных (файле Excel)
тег `path` содержит в имя файла Excel. Имя файла должно обязательно содержать в себе расширение .xlsx (.xls опционально)
тег sheetNumber сожержит в себе номер страницы на которой необходимо открыть файл с данными

далее идет тег columns которых содержит в себе теги `column`, их может быть сколь угодно много. 

Опишем содержимое тега column
```
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
|colType|описывает к какому типу будет преобразовано значение из этой колонки. Принимает значение int str float|
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

#### cropEnd

принимает значением только число и обрезает указанное значение от конца строки, например если вы хотите включить данный тег то указываете
в свойстве значение я true (это относится ко всем тегам со свойствами) например
<cropEnd mode="true">2</cropEnd>
если вам не нужен этот тег то оставляете как есть
<cropEnd mode="false"></cropEnd>
смысл работы данного тега такой: если например у вас попала строка "Привет" и вы включили этот тег и указали 2 то в результате строка превратится в "Приве"


#### addValueEnd

добавляет строку после значения из поля, например если вы указали <addValueEnd mode="true"> мир!</addValueEnd> (пробелы сохраняются) и попалась 
строка "Привет" то в результате получится "Привет мир!"

#### takeFromBegin

принимает как значение число,он берет начало строки до указанного значения. Например если строка "Привет" а в теге 2 то получится на выходе "Пр"

#### cropBegin

принимает как значение число. Этот тег возращает строку начиная с этого числа до конца строки, например "Привет" а в теге 2 то получится на выходе "ивет"

#### addValueBegin

принимает на вход строку. Этот тег добавляет в начала строки строку указанную в теге, например к строке "мир!" а в теге указать 
<addValueBegin mode="true">Привет </addValueBegin> то на выхоже получится "Привет мир!"

#### addValueBoth

принимает две строки на вход через запятую. Этот тег добавляет первую строчку в начало строки а вторую в конец.
Например <addValueBoth mode="true">Привет, мир!</addValueBoth> к строке ",чудесный" получится на выходе "Привет, чудесный мир!"

#### replace

отвечает за замену значения на другое значение. Если тег выключен то тег имеет вид `<replace mode="false"></replace>`
Но если вы хотите чтобы значения заменялись в этой строке то нужно включить этот тег прописав `mode="true"`
После включения этого тега вам нужно теперь добавить теги для замены, это делается следующим образом
```
                <replace mode="true"> 
                    <replaceVal>
                        <value>строка_которую_надо_заменить</value>
                        <toValue>строка_на_которую_надо_заменить</toValue>
                    </replaceVal>
                </replace>
```
блок `replaceVal` включает в себя два тега *value* и *toValue*. Тег *value* принимает строку которую нужно заменить а тег *toValue* включает в себя строку на которую нужно заменить
блоков *replaceVal* может быть сколь угодно много, например
```
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

#### Порядок выполнения преобразования

Если включить все теги `cropEnd addValueEnd takeFromBegin cropBegin addValueBegin addValueBoth replace` то они все обработают полученную строку
Порядок выполнения операций обработки: cropEnd, cropBegin, addValueEnd, takeFromBegin, addValueBegin, addValueBoth, replace

#### Примечание

Надо учесть, что блоков `column` в теге `importXml` может быть больше чем колонок в файле Excel, это возникает в том случае, если одна и таже колонока
идет в разные поля в базе данных. Например
```
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
            </column>
```

В поле `colName` в обоих случаях прописывается имя этой колонки, но в поле `colNameDb` надо указать в каждом блоке имя поля в которое пойдет это значение.
Но количество блоков column в теге `exportTable` должно быть ровно таким сколько полей в базе данных.

## тег linkedColumns

этот тег нужен для режима сравения двух файлов 
Он работает только в режиме `<checkMode>true</checkMode>`. В режиме загрузки *insert* ставим `<checkMode>false</checkMode>` а `<linkedColumns mode="false">`

```
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

## тег withDict

он нужен для описания словарной таблицы из которой будет браться индекс

```
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
                                <colType></colType> <!-- str / int / float -->
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

### тег exportTable

Этот блок описывает поля базы данных

```
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
Структура тега column следующая 
```
            <column>
                <name>имя_поля_в_базе_данных</name>
                <isAutoInc>является_ли_поле_в_базе_автоинкрементом</isAutoInc>
                <isConc>введено_для_составных_полей_из_нескольких_колонок_но_пока_не_поддерживается</isConc>
                <fromExcel>берется_ли_поле_из_файла_или_дефолтное</fromExcel>
                <defaultValue mode="false\true">дефолтное_значение</defaultValue>
                <colType>str\int</colType>
                <ifNull mode="true\false">значение_если_поле_null</ifNull>
            </column>
```
тег name включает в себя имя поля в базе данных

тег isAutoInc характеризует является ли данное поле автоинкрементом в базе данных, если значение false то значит что это поле не автоинкремент а если true то значит
что это поле автоинкремент
Если поле автоинкремент то оно просто не включается в запрос на вставку

тег isConc пока не поддерживается и он всегда <isAutoInc>false</isAutoInc>

тег fromExcel описывает берется ли данное поле из файла или он заполняется дефолтным значением

тег defaultValue принимает в себя строку, которую нужно вставлять когда поле не берется из файла. Например 
```
<fromExcel>false</fromExcel>
<defaultValue mode="true">null</defaultValue> 
```
то значит это поле будет заполняться null'ами

тег colType описывает какого типа будут вставляться строчки. Принимает значение int или str.По сути это значит будет ли вставляемое значение оборачиваться в кавычки или нет. Если поле берется не из файла и по дефолту вставляется null то нужно заполнить это поле значением int так как null в ковычках будет приниматься как строка т.е.
```
<fromExcel>false</fromExcel>
<defaultValue mode="true">null</defaultValue>
<colType>int</colType>
```
тег ifNull нужен для того, чтобы заменять поля получаемые из базы на другие значение,если они становятся налами. Например

```
<fromExcel>true</fromExcel>
<defaultValue mode="false"></defaultValue>
<colType>str</colType>
<ifNull mode="true">null</ifNull>
```
То это значит, что полученное значение в случае null заменится на null. Тут в запросе нал будет вставляться без ковычек даже если поле строковое.


В тег exportTable в блок описания столбцов в применике были добавлены следующие теги

fromDb указывает на то берется ли значение из словарной таблицы в базе. true если берется
isUpdateCondition работает в режиме <loadMode>update</loadMode> если <isUpdateCondition>true</isUpdateCondition> то эта колонка податает в условие WHERE в апдейте и по ней будут искаться колонки для апдейта
Если <ifNull mode="false"></ifNull> и одновременно <defaultValue mode="false"></defaultValue> и колонка берется из экселя то эта колонка будет проверяться на налы

isConc теперь работает. Если <isConc>true</isConc> то просто в описании колонок в источнике в блоке importXml указываем имя этой колонки в тех колонках которые хотим соединить и они автоматически сверху вниз в порядке следования в конфиге соединятся













