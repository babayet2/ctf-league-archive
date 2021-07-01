<?php 
require_once 'config.php';
include 'header.php';

if (is_logged_in()) {
?>

<h2>Welcome, <?php echo htmlentities($_SESSION['username']); ?></h2>
<form action="/" method="GET">
    <h3>What would you like to make the cow say?</h3>
    <input type="text" name="message" value="<?php echo (!isset($_GET['message']) ? "Hello, world!" : htmlentities($_GET['message'])); ?>">
    <input type="submit">
</form>

<?php
    if (isset($_GET['message'])) {
        echo '<br><pre>';
        echo "$ cowsay '" . htmlentities($_GET['message']) . "'\n";
        // echo htmlentities(shell_exec("echo '" . $_GET['message'] . "' | sed -e '/MESSAGE/{r /dev/stdin' -e 'd;}' /cowsay.txt"));
        echo htmlentities(shell_exec("/usr/local/bin/cowsay '" . $_GET['message'] . "'"));
        echo '</pre><br><p>Note: Flag is stored at /flag.txt on the webserver.</p>';
    }
} else {
?>

<!-- lol sorry about the crappy php web app -->
<h2>Click <a href="login.php">here</a> to login</h2>
<script>window.location = "login.php";</script>

<?php
}
include 'footer.php';
?>
