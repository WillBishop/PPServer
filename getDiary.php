<?php
if ($_SERVER["REQUEST_METHOD"] === 'POST') {

  $required = array('username', 'password');

  $error = false;

  foreach($required as $field) { //Ensures all of the required POST fields are present.
    if (empty($_POST[$field])) {
      $error = true;
    }
  }
  if ($error) {
  header("HTTP/1.1 400");} //Else, header bad request.
  else {
    $username = $_POST["username"];
    $password = $_POST["password"];
    $year = $_POST["year"];
    $classes = shell_exec("python3 getDiary.py '$username' '$password'"); //String encodes username and password, because some students had characters in their passwords that where also used in Bash.
    $response = str_replace("'", "\"",$classes);
    if (strpos($response, "ITWASASUCCESS") !== true){//In python, if the request is not successful, it prints the status code, this relays that to the client.
      header("HTTP/1.1 $response");
    }
    if (strpos($response, "ITWASASUCCESS") !== false){
      $result = str_replace("ITWASASUCCESS", "", $response);
      echo $result;
      
  }}} 
else {
  header("HTTP/1.1 405"); //Method not allowed, POST only.
  }

?>