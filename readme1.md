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