<?php
require 'config.php';
include 'header.php';
?>

<?php
if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    #$password = password_hash($_POST['password'], PASSWORD_DEFAULT);
    $password = $_POST['password'];

    $query_str = "SELECT id, username, password FROM users WHERE username='$username' AND password='$password';";
     // what is password hashing???????????????
    echo '* <b>Query:</b> ' . htmlentities($query_str) . '<br>';


    $conn = get_connection();
    $result = $conn->query($query_str);
    echo '* <b>Results:</b><br>';
    $login_success = false;
    if ($result->num_rows > 0) {
        echo '<table>';
        echo '<tr><th>id</th><th>username</th><th>password</ht></tr>';
        while ($row = $result->fetch_assoc()) {
            echo '<tr><td>' . htmlentities($row['id']) . '</td><td>' . htmlentities($row['username']) . '</td><td>%%REDACTED%%</td>' . '</tr>';

            //if (password_verify($_POST['password'], $row['password'])) {
                $login_success = true;
                $username = $row['username'];
                $_SESSION['username'] = $row['username'];
            //}
        }
        echo '</table><br><br>';
    } else { echo '(none)'; }

    echo '<h3>Login attempt ' . ($login_success ? 'successful. <a href="/">Click here</a> to continue.<script>window.location = "index.php";</script>' : 'failed.') . '</h3><br><hr><br>';
}
?>

<!-- don't mind how poorly written this website is -->
<h3>Ha! SQL injection? Who cares. If we had to fix *every* vulnerability, we may as just live in a cave!</h3><br>
<p>Figure out how to login without knowing the username or password!</p><br>

<form action="login.php" method="POST">
    <input type="text" name="username" placeholder="Username">
    <input type="password" name="password" placeholder="Password">
    <input type="submit">
</form>

<?php
include 'footer.php';
?>
