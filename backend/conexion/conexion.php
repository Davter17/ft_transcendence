<?php

$server="localhost";
$user="root";
$pass="";
$db="test";

$conexion = new mysqli($server, $user, $pass, $db);

if ($conexion->connect_errno)
	die("Failure conexion " . $conexion->connect_errno );
else
	return $conexion;

?>