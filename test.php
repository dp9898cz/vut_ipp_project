<?php

require_once("./test_library/args_checker.php");
require_once("./test_library/scanner.php");
require_once("./test_library/html_generator.php");

$arg_checker = new ArgumentChecker();
$arg_checker->checkArgs();

$scanner = new Scanner();
$scanner->scan($arg_checker->directory, $arg_checker->run_recursively);

$number_of_tests = 0;
$failed_tests = 0;

foreach ($scanner->folders as $folder) {
    foreach($scanner->files[$folder] as $file) {
        $number_of_tests++;

        $source = $folder.$file['name'].'.src';
        $input = $folder.$file['name'].'.in';
        $return = $folder.$file['name'].'.rc';
        $output = $folder.$file['name'].'.out';

        //TODO parse only, int only

        unset($parse_out);
        unset($parse_retval);
        exec("php7.4 " . $arg_checker->parse . " < " . $source , $parse_out, $parse_retval);
        
        if ($parse_retval == 0) {
            unset($int_out);
            unset($int_retval);
            exec("php7.4 " . $arg_checker->parse . " < " . $source . " 2>/dev/null | python3.8 " . $arg_checker->interpret . " --input=" . $input , $int_out, $int_retval);

            if (($int_retval == 0) && ($int_retval == file_get_contents($return))) {
                //interpretation complted, now we have to compare the output
                unset($diff_retval);
                exec("php7.4 " . $arg_checker->parse . " < " . $source . " 2>/dev/null | python3.8 " . $arg_checker->interpret . " --input=". $input . " 2>/dev/null | diff " . $output . " -", $diff_out, $diff_retval);
                if ($diff_retval == 0) {
                    $scanner->save_test_output($folder, $file['name'], $parse_retval, $int_retval, true);
                }
                else {
                    $scanner->save_test_output($folder, $file['name'], $parse_retval, $int_retval, false);
                    $failed_tests++;
                }
            }
            elseif (($int_retval != 0) && ($int_retval == file_get_contents($return))) {
                //interpretation failed but it was intended
                $scanner->save_test_output($folder, $file['name'], $parse_retval, $int_retval, true);
            }
            else {
                //not completed test
                $scanner->save_test_output($folder, $file['name'], $parse_retval, $int_retval, false);
                $failed_tests++;
            }
        }
        else {
            //there was some error during parsing
            if ($parse_retval == file_get_contents($return)) {
                $scanner->save_test_output($folder, $file['name'], $parse_retval, '', true);
            }
            else {
                $scanner->save_test_output($folder, $file['name'], $parse_retval, '', false);
                $failed_tests++;
            }
            
        }
    }
}

//now we have to process the html page
$generator = new HTML_generator($scanner, $number_of_tests, $failed_tests);
$generator->generate();

?>