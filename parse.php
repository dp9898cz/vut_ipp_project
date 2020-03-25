<?php
/** skript parse.php do předmětu IPP */
/** autor: Daniel Pátek (xpatek08) */
/** VUT FIT */

/**
 * skript parse.php do předmětu IPP 
 * @author Daniel Pátek (xpatek08)
 * VUT FIT
 */

define('ERR_OK', 0);
define('ERR_BAD_ARGS', 10);
define('ERR_HEAD_MISS', 21);
define('ERR_BAD_CODE', 22);
define('ERR_CODE_OTHER', 23);

const TOKEN_EOF = 11;
const TOKEN_CONST = 12;
const TOKEN_VAR = 13;
const TOKEN_HEADER = 14;
const TOKEN_LABEL = 15;
const TOKEN_INSTRUCTION = 16;
const TOKEN_TYPE = 17;

$instruction_list = array(
"MOVE",        //0
"CREATEFRAME", //1
"PUSHFRAME",
"POPFRAME",
"DEFVAR",
"CALL",        //5
"RETURN",
"PUSHS",
"POPS",
"ADD",
"SUB",         //10
"MUL",
"IDIV",
"LT",
"GT",
"EQ",          //15
"AND",
"OR",
"NOT",
"INT2CHAR",
"STRI2INT",    //20
"READ",
"WRITE",
"CONCAT",
"STRLEN",
"GETCHAR",     //25
"SETCHAR",
"TYPE",
"LABEL",
"JUMP",
"JUMPIFEQ",    //30
"JUMPIFNEQ",
"EXIT",
"DPRINT",
"BREAK"        //34
);


$stderr = fopen('php://stderr', 'w');
$stdout = fopen('php://stdout', 'w');
$stdin = fopen('php://stdin', 'r');

check_args($argc, $argv);

//create DOM document
$dom_docu = new DOMDocument('1.0', 'UTF-8');
$dom_docu->formatOutput = true;

//create XML program syntax
$xml_final = $dom_docu->createElement('program');
$xml_final->setAttribute('language', 'IPPcode20');
$xml_final = $dom_docu->appendChild($xml_final);

//run the syntax check
check_syntax_build_xml();

//print the XML to stdout
echo $dom_docu->saveXML();

exit(ERR_OK);


/** 
 * Funkce pro kontrolu argumentů a vypsání help
 * @param int $argc Počet argumentů při spuštění programu
 * @param string $argv Pole argumentů ve formátu string
*/
function check_args($argc, $argv) {
    global $stderr;

    for ($i=1; $i < $argc; $i++) { 
        if ($argv[$i] == "--help") {
            if ($argc > 2) {
                fwrite($stderr, "Nemuzete zadat vice argumentu spolecne s \"--help\".\n");
                exit(ERR_BAD_ARGS);
            }
            echo "Skript typu filtr (parse.php v jazyce PHP 7.4)\n";
            echo "nacte ze standardniho vstupu zdrojovy kod v IPPcode20\n";
            echo "zkontroluje lexikalni a syntaktickou spravnost kodu\n";
            echo "a vypise na standardni vystup XML reprezentaci programu.\n";
            exit(ERR_OK);
        }
    }
}

/**
 * Syntaktická kontrola zdrojového kódu a tvorba XML reprezentace programu
 */
function check_syntax_build_xml() {
    
    global $stderr;
    global $instruction_list;
    global $dom_docu;
    global $xml_final;

    $inst_counter = 0;

    $analyzed_sentence = array(); //array

    //first we have to check the header
    $analyzed_sentence = next_sentence_scan();
    if ($analyzed_sentence[0] != NULL) {
        if ($analyzed_sentence[0][0] != NULL) {
            if ($analyzed_sentence[0][0] != TOKEN_HEADER) {
                fwrite($stderr, "Chybi spravna hlavicka (ippcode20).\n");
                exit(ERR_HEAD_MISS);
            }
        }
        else {
            fwrite($stderr, "Vyskytla se neocekanava chyba.\n");
            exit(ERR_CODE_OTHER);
        }
    }
    else {
        fwrite($stderr, "Vyskytla se neocekanava chyba.\n");
        exit(ERR_CODE_OTHER);
    }

    //start to check instructions and generate xml code
    while ($analyzed_sentence[0][0] != 11) {
        //take the first sentence
        $analyzed_sentence = next_sentence_scan();

        switch ($analyzed_sentence[0][0]) {
            case TOKEN_HEADER:
                fwrite($stderr, "Hlavicka je umistena na nespravnem miste.\n");
                exit(ERR_CODE_OTHER);
            
            case TOKEN_EOF:
                break;
            
            case TOKEN_INSTRUCTION:
                break;

            default:
                fwrite($stderr, "Vyskytla se syntakticka chyba pri zpracovani syntaxe.\n");
                exit(ERR_BAD_CODE);
        }

        if ($analyzed_sentence[0][0] == TOKEN_EOF) {
            break;
        }
        elseif ($analyzed_sentence[0][0] == TOKEN_INSTRUCTION) {

            $inst_counter++;

            //create xml instruction
            $instruction = $dom_docu->createElement("instruction");
            $instruction->setAttribute("order", $inst_counter);
            $instruction->setAttribute("opcode", $instruction_list[$analyzed_sentence[0][1]]);
            
            //check the args of each instruction
            switch ($analyzed_sentence[0][1]) {
                case 1: case 2: case 3: case 6: case 34:
                    //now we have to make sure that there is no operand
                    //CREATEFRAME PUSHFRAME POPFRAME RETURN BREAK
                    check_instr_number_args($analyzed_sentence, 0);
                break;
                
                case 4: case 8:
                    //these are instructions with one var operand
                    //DEFVAR POPS
                    //first check the number of args
                    check_instr_number_args($analyzed_sentence, 1);

                    //check if it correct argument
                    check_instr_type_arg($analyzed_sentence, TOKEN_VAR);

                    //add xml type of arg to xml documnet (as child of the current instruction)
                    $var_arg = $dom_docu->createElement("arg1", htmlspecialchars($analyzed_sentence[1][1]));
                    $var_arg->setAttribute("type", "var");
                    $instruction->appendChild($var_arg);
                break;
                    //next check types
                case 5: case 28: case 29:
                    //one operand instruction with LABEL operand
                    //CALL LABEL JUMP
                    //first check the number of args
                    check_instr_number_args($analyzed_sentence, 1);

                    //then check the argument label
                    check_instr_type_arg($analyzed_sentence, TOKEN_LABEL);

                    //add xml type of arg to xml documnet (as child of the current instruction)
                    $var_arg = $dom_docu->createElement("arg1", htmlspecialchars($analyzed_sentence[1][1]));
                    $var_arg->setAttribute("type", "label");
                    $instruction->appendChild($var_arg);
                break;

                case 7: case 22: case 32: case 33:
                    //one operand instruction with SYMB operand
                    //PUSHS WRITE EXIT DPRINT
                    //check the number of args
                    check_instr_number_args($analyzed_sentence, 1);
                    
                    //check const argument
                    check_symb_arg($analyzed_sentence[1], $analyzed_sentence[0][1]);

                    //add xml type of arg to xml documnet (as child of the current instruction)
                    if ($analyzed_sentence[1][0] == TOKEN_VAR) {
                        $var_arg = $dom_docu->createElement("arg1", htmlspecialchars($analyzed_sentence[1][1]));
                        $var_arg->setAttribute("type", "var");
                    }
                    else {
                        $var_arg = $dom_docu->createElement("arg1", htmlspecialchars($analyzed_sentence[1][2]));
                        $var_arg->setAttribute("type", $analyzed_sentence[1][1]);
                    }

                    $instruction->appendChild($var_arg);
                break;

                case 0: case 19: case 24: case 27: case 18:
                    //two args instructions
                    //MOVE INT2CHAR READ STRLEN TYPE NOT
                    //agr1: var arg2: symb
                    //check the number of args
                    check_instr_number_args($analyzed_sentence, 2);

                    //check the first argument
                    check_instr_type_arg($analyzed_sentence, TOKEN_VAR);

                    //check the second argumnet
                    check_symb_arg($analyzed_sentence[2], $analyzed_sentence[0][1]);

                    //generate xml arg1
                    $var_arg = $dom_docu->createElement("arg1", htmlspecialchars($analyzed_sentence[1][1]));
                    $var_arg->setAttribute("type", "var");
                    $instruction->appendChild($var_arg);

                    //generate xml arg2
                    if ($analyzed_sentence[2][0] == TOKEN_VAR) {
                        $var_arg = $dom_docu->createElement("arg2", htmlspecialchars($analyzed_sentence[2][1]));
                        $var_arg->setAttribute("type", "var");
                    }
                    else {
                        $var_arg = $dom_docu->createElement("arg2", htmlspecialchars($analyzed_sentence[2][2]));
                        $var_arg->setAttribute("type", $analyzed_sentence[2][1]);
                    }
                    $instruction->appendChild($var_arg);
                break;

                case 21:
                    //just instruction READ
                    //arg1: var arg2: type
                    //check number and first agr
                    check_instr_number_args($analyzed_sentence, 2);
                    check_instr_type_arg($analyzed_sentence, TOKEN_VAR);

                    //check the type argumnent
                    if ($analyzed_sentence[2][0] == TOKEN_TYPE) {
                        $var_arg = $dom_docu->createElement("arg1", htmlspecialchars($analyzed_sentence[1][1]));
                        $var_arg->setAttribute("type", "var");
                        $instruction->appendChild($var_arg);

                        $var_arg = $dom_docu->createElement("arg2", htmlspecialchars($analyzed_sentence[2][1]));
                        $var_arg->setAttribute("type", "type");
                        $instruction->appendChild($var_arg);
                    }
                    else {
                        fwrite($stderr, "Druhy argument u instrukce TYPE musi byt typ. (string, int, bool, nil)\n");
                        exit(ERR_CODE_OTHER);
                    }
                break;

                case 9: case 10: case 11: case 12: case 13: case 14: case 15: case 16: case 17: case 20: case 23: case 25: case 26:
                    // ADD SUB MUL IDIV LT GT EG AND OR
                    //check number and first arg
                    check_instr_number_args($analyzed_sentence, 3);
                    check_instr_type_arg($analyzed_sentence, TOKEN_VAR);

                    //check the second and third argument
                    check_symb_arg($analyzed_sentence[2], $analyzed_sentence[0][1]);
                    check_symb_arg($analyzed_sentence[3], $analyzed_sentence[0][1]);

                    //generate first xml
                    $var_arg = $dom_docu->createElement("arg1", htmlspecialchars($analyzed_sentence[1][1]));
                    $var_arg->setAttribute("type", "var");
                    $instruction->appendChild($var_arg);

                    //generate xml for the second argument
                    if ($analyzed_sentence[2][0] == TOKEN_VAR) {
                        $var_arg = $dom_docu->createElement("arg2", htmlspecialchars($analyzed_sentence[2][1]));
                        $var_arg->setAttribute("type", "var");
                    }
                    else {
                        $var_arg = $dom_docu->createElement("arg2", htmlspecialchars($analyzed_sentence[2][2]));
                        $var_arg->setAttribute("type", $analyzed_sentence[2][1]);
                    }
                    $instruction->appendChild($var_arg);

                    //generate xml for the third argument
                    if ($analyzed_sentence[3][0] == TOKEN_VAR) {
                        $var_arg = $dom_docu->createElement("arg3", htmlspecialchars($analyzed_sentence[3][1]));
                        $var_arg->setAttribute("type", "var");
                    }
                    else {
                        $var_arg = $dom_docu->createElement("arg3", htmlspecialchars($analyzed_sentence[3][2]));
                        $var_arg->setAttribute("type", $analyzed_sentence[3][1]);
                    }
                    $instruction->appendChild($var_arg);
                break;

                case 30: case 31:
                    //JUMPIFEQ JUMPIFNEQ
                    //check number and first arg
                    check_instr_number_args($analyzed_sentence, 3);
                    check_instr_type_arg($analyzed_sentence, TOKEN_LABEL);

                    //check the second and third argument
                    check_symb_arg($analyzed_sentence[2], $analyzed_sentence[0][1]);
                    check_symb_arg($analyzed_sentence[3], $analyzed_sentence[0][1]);

                    //generate first xml
                    $var_arg = $dom_docu->createElement("arg1", htmlspecialchars($analyzed_sentence[1][1]));
                    $var_arg->setAttribute("type", "label");
                    $instruction->appendChild($var_arg);

                    //generate xml for the second argument
                    if ($analyzed_sentence[2][0] == TOKEN_VAR) {
                        $var_arg = $dom_docu->createElement("arg2", htmlspecialchars($analyzed_sentence[2][1]));
                        $var_arg->setAttribute("type", "var");
                    }
                    else {
                        $var_arg = $dom_docu->createElement("arg2", htmlspecialchars($analyzed_sentence[2][2]));
                        $var_arg->setAttribute("type", $analyzed_sentence[2][1]);
                    }
                    $instruction->appendChild($var_arg);

                    //generate xml for the third argument
                    if ($analyzed_sentence[3][0] == TOKEN_VAR) {
                        $var_arg = $dom_docu->createElement("arg3", htmlspecialchars($analyzed_sentence[3][1]));
                        $var_arg->setAttribute("type", "var");
                    }
                    else {
                        $var_arg = $dom_docu->createElement("arg3", htmlspecialchars($analyzed_sentence[3][2]));
                        $var_arg->setAttribute("type", $analyzed_sentence[3][1]);
                    }
                    $instruction->appendChild($var_arg);
                break;

                default:
                    # code...
                    break;
            }
        }
        else {
            fwrite($stderr, "Vyskytla se syntakticka chyba pri zpracovani syntaxe[1].\n");
            exit(ERR_BAD_CODE);
        }

        $xml_final->appendChild($instruction);
    }
    
}

/**
 * Lexikální kontrola zdrojového kódu a tvorba pole objektů na aktuálním řádku
 * @return array $prepared_sentence Pole objektů na aktuálním řádku
 */
function next_sentence_scan() {
    global $stderr;
    global $stdin;

    $prepared_sentence = array(); //this goes back to syntax_parser (array of arrrays)

    $start_sentense = true; //when im on the start of sentence, i have to check instruction

    while (true) {  
        //checking EOF
        if (($sentence = fgets($stdin)) == false) {
            array_push($prepared_sentence, array(TOKEN_EOF));
            return $prepared_sentence;
        }

        //check if the sentence is comment or just newline
        if (preg_match('~^\s*#~', $sentence) || preg_match('~^\s*$~', $sentence)) {
            continue;
        }

        //check that the line does not have comment at the end, takes just the first part
        //make array of words and delete "" content
        $split_comment = explode('#', $sentence);
        $split_word = preg_split('~\s+~', $split_comment[0]);
        if (end($split_word) == "") {
            array_pop($split_word);
        }
        if ($split_word[0] == "") {
            array_shift($split_word);
        }

        break;
    }
    foreach($split_word as $word) {

        if (preg_match('~@~', $word)) {
            //will be bool, string, int nebo nil [constant]
            if (preg_match('~^(int|bool|nil|string)~', $word)) {
                //check the lexem
                if (
                    preg_match('~^int@[+-]?[0-9]+$~', $word) ||
                    preg_match('~^nil@nil$~', $word) ||
                    preg_match('~^bool@(true|false)$~', $word) ||
                    preg_match('~^string@$~', $word) ||
                    (preg_match('~^string@~', $word) &&
                    !preg_match('~(\\\\($|\p{S}|\p{P}\p{Z}|\p{M}|\p{L}|\p{C})|(\\\\[0-9]{0,2}($|\p{S}|\p{P}\p{Z}|\p{M}|\p{L}|\p{C}))| |#)~', $word))
                ) {
                    //now we have completed lexical analysis of constant       [\u0000-\u002F\u003A-\uFFFF]
                    $type_and_data = explode('@', $word, 2);
                    $final = array();
                    array_push($final, TOKEN_CONST);
                    array_push($final, $type_and_data[0]);
                    array_push($final, $type_and_data[1]);
                    array_push($prepared_sentence, $final);
                }
                else {
                    fwrite($stderr, "Konstanta $word ma spatny format.\n");
                    exit(ERR_CODE_OTHER);
                }
            }
            else {
                //this could be variable
                if (preg_match('~^(GF|TF|LF)@[a-zA-Z_\-$&%*!?]*$~', $word)) {
                    array_push($prepared_sentence, array(TOKEN_VAR, $word));
                }
                else {
                    fwrite($stderr, "Konstanta $word ma spatny typ.\n");
                    exit(ERR_CODE_OTHER);
                }
            }
        }
        else {
            if (preg_match('~^(int|bool|string|nil)$~', $word)) {
                //this is just type
                array_push($prepared_sentence, array(TOKEN_TYPE, $word));
            }
            else {
                if (preg_match('~^\.ippcode20$~i', $word)) {
                    //this is header
                    array_push($prepared_sentence, array(TOKEN_HEADER));
                }
                else  {
                    //now i have to check whether its instruction or label
                    $instr_number = -1;
                    $instr_number = find_instruction($word);
                    if ($instr_number != -1 && $start_sentense == true) {
                        //found instruction
                        array_push($prepared_sentence, array(TOKEN_INSTRUCTION, $instr_number));
                    }
                    else {
                        //it has to be label now
                        if (preg_match('~^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$~', $word)) {
                            array_push($prepared_sentence, array(TOKEN_LABEL, $word));
                        }
                        else {
                            //error
                            fwrite($stderr, "Nerozpoznane slovo \"$word\", lexikalni chyba.\n");
                            exit(ERR_BAD_CODE);
                        }
                    }
                }
            }
        }
        //back to another word
        $start_sentense = false;
    }
    //array_push($prepared_sentence, array('ajjja', 10));
    return $prepared_sentence;
}

/**
 * Hledá slovo v seznamu instrukcí
 * @param string $word Potenciální instrukční slovo
 * @return int Číslo instrukce (-1 pro nenalezeno)
 */
function find_instruction($word) {
    global $instruction_list;

    for ($i=0; $i <= 34; $i++) { 
        if (strcasecmp($word, $instruction_list[$i]) == 0){
            //return number of instruction
            return $i;
        }
    }
    //didnt find any instruction with that name
    return -1;
}

/**
 * Kontrola počtu argumentů u instrukce
 * @param array $some_sentence Aktuální věta tvořená objekty (intrukcí a argumenty)
 * @param int $number Správný počet argumentů instrukce
 */
function check_instr_number_args($some_sentence, $number) {
    global $stderr;
    global $instruction_list;
    
    if (count($some_sentence) != ($number + 1)) {
        $obj = $instruction_list[$some_sentence[0][1]];
        if ($number == 1) {
            fwrite($stderr, "Instrukce $obj musí mít pouze jeden argument.\n");
        }
        else if ($number == 0) {
            fwrite($stderr, "Instrukce $obj nesmí mít žádný argument.\n");
        }
        else {
            fwrite($stderr, "Instrukce $obj musí mít přesně $number argumenty.\n");
        }
        exit(ERR_CODE_OTHER);
    }
}

/**
 * Kontrola typu prvního argumentu u instrukce na aktuálním řádku
 * @param array $another_sentence Aktuální věta (intrukce), tvořená objekty
 * @param int $right_type Číslo správného typu (tokenu)
 */
function check_instr_type_arg($another_sentence, $right_type) {
    global $stderr;
    global $instruction_list;

    if ($another_sentence[1][0] != $right_type) {
        $obj = $instruction_list[$another_sentence[0][1]];
        fwrite($stderr, "Instrukce $obj má špatný typ argumentu.\n");
        exit(ERR_CODE_OTHER);
    }
}


/**
 * Kontrola typu argumentu u instrukce na aktuálním řádku
 * @param array $another_object Aktuální argument instrukce
 * @param int $instruction_n Číslo instrukce
 */
function check_symb_arg($another_object, $instruction_n) {
    global $stderr;
    global $instruction_list;

    if ($another_object[0] != TOKEN_VAR && $another_object[0] != TOKEN_CONST) {
        $obj = $instruction_list[$instruction_n];
        fwrite($stderr, "Spatny typ argumentu u instrukce $obj.\n");
        exit(ERR_CODE_OTHER);
    }
}
?>