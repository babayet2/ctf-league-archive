<?php 

// show source if requested
if (isset($_GET['src'])) {
    show_source('index.php');
    die();
}

require_once 'config.php';
include 'header.php';

if (is_logged_in()) {
?>

<p>Welcome, <?php echo htmlentities($_SESSION['username']); ?></p>
<p style="margin-left: 35vw;margin-right: 35vw;">This part of the application is vulnerable to <a href="https://www.nuharborsecurity.com/web-application-security-insecure-direct-object-reference-IDOR">IDOR</a>. Figure out how to exploit it! CTF pro tip: it's always helpful to Google relevant terms from challenges + "ctf" to find resources and writeups from similar challenges!</p>
<p>The flag is stored in one of the first notes created (but by a different user)</p>
<!-- NOTE: IDOR vulnerabilities exist when access control is not properly implemented, and resource IDs are not unique enough / are guessable. i.e. the root cause is the improper access control / it's a type of access control issue. -->
<!-- also sorry about the poorly written / ugly web app. next time, it won't be in PHP, and it will have decent CSS :)  -->

<?php
    if (isset($_POST['title'])) {
        // insert into db
        $conn = get_connection();
        $stmt = $conn->prepare('INSERT INTO notes (userid, title, body) VALUES (?, ?, ?)');
        $title = ($_POST['title'] ? $_POST['title'] : '(empty)'); // wtf why can't PHP do $_POST['title'] || '(empty)'
        $body = ($_POST['body'] ? $_POST['body'] : '(empty)');
        $stmt->bind_param('iss', intval($_SESSION['userid']), $title, $body);
        $stmt->execute();

        // get most recent note id
        // XXX: use lastInsertId
        $stmt = $conn->prepare('SELECT id FROM notes WHERE userid=? ORDER BY id DESC LIMIT 1');
        $stmt->bind_param('i', intval($_SESSION['userid']));
        $stmt->execute();
        $stmt->bind_result($noteid);
        $stmt->fetch();
        echo '<script>window.location = "note.php?id=' . htmlspecialchars('' . $noteid) . '";</script>Note created.';
    } else {
        $conn = get_connection();
        $stmt = $conn->prepare('SELECT id, title FROM notes WHERE userid=?');
        $stmt->bind_param('i', intval($_SESSION['userid']));
        $stmt->execute();
        $stmt->bind_result($noteid, $title);
        $output = '<h2>Your notes</h2><div>';
        $n_notes = 0;
        while ($stmt->fetch()) {
            // XXX: use <ul>/<li>
            $output .= '* <a style="font-family: monospace;" href="note.php?id=' . $noteid . '">' . htmlspecialchars($title) . '</a><br>';
            $n_notes++;
        }
        $output .= '</div>';
        
        // only show notes if there are any
        if ($n_notes) {
            echo $output;
        }
    }
?>


<form action="/" method="POST">
    <h2>Create a note</h2><br>
    <input style="font-family: monospace; width: 20vw;" type="text" name="title" placeholder="Enter a title here..." value="Title"><br>
    <textarea style="font-family: monospace; width: 20vw;" name="body">Hello, world!</textarea><br>
    <input type="submit"><br>
</form>

<?php 
} else {
?>

<!-- lol sorry about the crappy php web app -->
<h2>Click <a href="login.php">here</a> to login</h2>
<script>window.location = "login.php";</script>

<?php
}
include 'footer.php';
?>
