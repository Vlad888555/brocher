<?php
include "DB.php";
$db = new DB();


$name = $_POST["name"];
$password = $_POST["password"];

$db->reg($name, $password);

header("Location: index.php");