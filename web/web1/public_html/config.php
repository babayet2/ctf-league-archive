<?php
session_start();

// ignore this crappy code
function get_connection() {
    $conn = new mysqli('mysql', 'root', 'lance_carry_our_crypto_plz', 'web1');

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    return $conn;
}

function is_logged_in() {
    return isset($_SESSION['username']);
}

?>
