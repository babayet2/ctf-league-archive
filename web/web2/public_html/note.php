<?php 
// show source if requested
if (isset($_GET['src'])) {
    show_source('note.php');
    die();
}

require_once 'config.php';
include 'header.php';

if (is_logged_in()) {
    if (isset($_GET['id'])) {
        $conn = get_connection();
        $stmt = $conn->prepare('SELECT id, title, body FROM notes WHERE id=?');
        $stmt->bind_param('i', intval($_GET['id']));
        $stmt->execute();
        $stmt->bind_result($noteid, $title, $body);
        if ($stmt->fetch()) {
            echo '<h2 style="margin-bottom: -0.2em;"><a style="font-family: monospace;" href="note.php?id=' . $noteid . '">' . htmlspecialchars($title) . '</a></h2><p><i>created by you</i></p><br><div style="font-family: monospace;margin-left: 35vw;margin-right: 35vw;">' . htmlspecialchars($body) . '</div>';
        } else {
            echo 'Note not found.<script>window.location = "index.php";</script>';
        }
    } else {
        echo 'Please specify a note id.<script>window.location = "index.php";</script>';
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
