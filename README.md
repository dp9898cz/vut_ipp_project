# Implementační dokumentace k 1. úloze do IPP 2019/2020
jméno a příjmení: __Daniel Pátek__ 
login: __xpatek08__
### 1. Úvod
Zadání bylo naimplementovat v jazyce PHP 7.4 skript parse.php , který bude provádět lexikální a syntaktickou analýzu jakzyka IPPcode20.
### 2. Implementace
Skript parse.php čte zdrojový kód jazyka IPPcode20 ze standartního vstupu. Výstupem je XML reprezentace programu, která je vypsána na standartní výstup. Chybová hlášení jsou vypisována na standartní chybový výstup.   
Základem řešení je použití třídy `DOMdocument`, která zajišťuje sestavení a generování XML kódu.  
Syntaktickou kontrolu skript provádí ve funkci `check_syntax_build_xml()`. V této funkci rovněž připravuje XML kód pro následné vygenerování. Syntaktická kontrola probíhá formou konečného  implementovaným pomocí cyklu. Při každé iteraci požádá funkci `next_sentence_scan()` o zpracovaný další řádek kódu. Na základě typu instrukce se tedy ověří syntaxe (počet a typ argumentů instrukce) a pomocí funkcí třídy `DOMdocument` se vytvoří nový objekt s případnými parametry. 
Lexikální analýza probíhá při každem volání funkce `next_sentence_scan()`. Tato funkce je volána z funkce pro syntaktickou kontrolu. Vrací pole objektů, které se vyskytují na aktuálním řádku zdrojového kódu (instrukce a argumenty). Každý objekt má své číslo, podle toho, o který typ (token) se jedná. Funkce řádek rozdělí na jednotlivá slova, která následně kontroluje pomocí regexu a skládá z nich pole objektů. Samozřejmě ingnoruje komentáře a bílé znaky.     

# Implementační dokumentace k 2. úloze do IPP 2019/2020
jméno a příjmení: __Daniel Pátek__ 
login: __xpatek08__
### 1. Úvod
Zadání bylo naimplementovat v jazyce Python 3.8 skript `interpret.py` a v jazyce PHP 7.4 skript `test.php`. Skript `interpret.py` bude provádět analýzu a interpretaci XML souboru s programem. Skript `test.php` bude testovat oba předchozí skripty a bude generovat výstup ve formátu HTML5.
### 2. Implementace skriptu `interpret.py`
Skript `interpret.py` čte vstup buď ze souboru, nebo ze standartního vstupu. Výstupem je provedení samotného interpretovaného programu, případně jeho vypsání na standartní výstup. Chybová hlášení jsou vypisována na standartní chybový výstup.   
Hlavní tělo skriptu je v mém řešení v souboru `interpret.py`. Nejprve je zapotřebí zkontrolovat argumenty. K tomu slouží třída `ArgsChecker`. Zajišťuje správné přiřazení hodnot zadaných argumenty programu a výpis pomocného textu.   
Následně je nutné zkontrolovat a získat data z XML reprezentace programu, jenž má být interpretován. Tento problém řeší třída `XMLparser`, která s pomocí tří funkcí zkontroluje integritu XML souboru a také instrukcí v něm obsažených. S pomocí funkce `importInstructions()` jsou tyto instrukce importovány do listu instrukcí, aby mohly být dále použity.   
Samotná interpretace probíhá formou (ne)konečného cyklu. Při každém průchodu je zpracována jedna instrukce z listu instrukcí. Jsou použity třídy `InstructionList` pro práci se seznamem instrukcí a zjištění následující instrukce, třída `Instruction` pro uchování dat instrukce v strukturované podobě a třída `Frame` pro práci s rámci. K uchovaní dat v zásobníku je použito pole `dataStack`. Cyklus interpretace končí buď chybou a výpisem chyby nebo vyčerpáním listu instrukcí a ukončením s návratovým kódem 0.
### 2. Implementace skriptu `test.php`
Skript `test.php` hledá testové soubory buď v aktuálním adresáři, nebo v zadaném adresáři a provede jejich otestování. Výstupem je přehledná tabulka ve formátu HTML5, která je vypsána na standartní výstup. Chybová hlášení jsou vypisována na standartní chybový výstup.   
Skript se skládá z několika různých modulů. Hlavní `test.php` zajišťuje samotné testování a uchování výsledků testu. Dále `args_checker.php` slouží ke kontrole argumentů programu a přiřazení cest k souborům, `scanner.php` je důležitá část programu, která vyhledává testovací položky a případně vytváří chybějící soubory, a `html_generator.php` starající se o generování výsledné HTML stránky.   
Nejprve se ověří argumenty programu a zmapují se testové soubory `.src` v zadaném adresáři. K těmto souborům se případně vytvoří prázdné přídavné soubory `.in` a `.out`. Soubor `.rc` s návratovou hodnotou skriptu se případně vytvoří s hodnotou `0`.    
Následně se pokračuje samotným testováním. Nejprve se testuje skript `parse.php`. Na základě návratového kódu se následně testuje interpretace skriptem `interpret.py`. Výsledky se hned vyhodnotí a uloží se pro další zpracování.   
Po dokončení testování se vygeneruje výsledná HTML stránka s přehledným zabrazením výsledků testů.