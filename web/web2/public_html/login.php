<?php
// show source if requested
if (isset($_GET['src'])) {
    show_source('login.php');
    die();
}

require 'config.php';
include 'header.php';
?>

<?php

/*
 * ok, so what can you do here? You're able to execute arbitrary queries—thanks
 * to the SQL injection vuln—and tell whether or not there are results. How can
 * you exfiltrate useful information from the database using that?
 *
 * NOTE: Check out the LIKE clause!
 *   SELECT * FROM users WHERE password LIKE 'asdf%';
 * 
 * You'll probably need to write a Python script to do this. I would recommend
 * exfiltrating the username before the password, then updating your exfil 
 * query to be more specific about the user whose password you're exfiltrating.
 * Why? Otherwise, your exfil query's password-leaking conditions will be 
 * tested against multiple users, so you'll get weird results from your script.
 *
 */

// check if this is a POST request (if the user is trying to login)
if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    //$password = password_hash($_POST['password'], PASSWORD_DEFAULT);
    $password = $_POST['password'];

    // build query
    // XXX: this is vuln to SQL injection!
    $query_str = "SELECT id, username, password FROM users WHERE username='$username';";
    echo '* <b>Query:</b> ' . htmlentities($query_str) . '<br>';
    
    $conn = get_connection();
    $result = $conn->query($query_str);
    $login_success = false;

    // check if any rows were returned?
    if ($result->num_rows > 0) {
        // iterate over each row
        while ($row = $result->fetch_assoc()) {
            // compare the password hash stored in the database with the submitted password
            // if (password_verify($_POST['password'], $row['password'])) {
            if ($password === $row['password']) { // XXX: TODO implement password hashing
                $login_success = true;
                $username = $row['username'];
                $_SESSION['username'] = $row['username'];
                $_SESSION['userid'] = $row['id'];
                echo '<b>Welcome! <a href="/">Click here</a> to continue.</b><script>window.location = "index.php";</script>';
            }
        }

        if (!$login_success) {
            // this message means there was at least one row returned from the database query
            echo '<b>That password is incorrect</b>';
        }
    } else {
        // this message means no rows were returned from the database query
        echo '<b>That user was not found</b>';
    }
}
?>

<!-- don't mind how poorly written this website is -->
<h3>How is SQL injection useful when the goal is not to simply get the query to return more results?</h3><br>
<p>This web application is vulnerable to boolean-based blind SQL injection. You'll probably find it useful to read the <a href="login.php?src">source code</a> of this application.</p><br>

<form action="login.php" method="POST">
    <input type="text" name="username" placeholder="Username">
    <input type="password" name="password" placeholder="Password">
    <input type="submit">
</form>

<?php
include 'footer.php';
?>
