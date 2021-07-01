DROP DATABASE IF EXISTS web2;
CREATE DATABASE web2;
USE web2;

CREATE TABLE `users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(500) NOT NULL,
    `password` VARCHAR(500) NOT NULL,
    KEY `id` (`id`) USING BTREE,
    PRIMARY KEY (`id`)
);

CREATE TABLE `notes` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `userid` INT NOT NULL,
    `title` VARCHAR(500) NOT NULL,
    `body` VARCHAR(5000) NOT NULL,
    KEY `id` (`id`) USING BTREE,
    PRIMARY KEY (`id`)
);

INSERT INTO users (username, password) VALUES ('aaron', 'extr3me1y_s3cure');
INSERT INTO users (username, password) VALUES ('hadi', 'h3y_h@di123');
INSERT INTO users (username, password) VALUES ('zander', '8a6sd7saagc9a');
INSERT INTO users (username, password) VALUES ('lance', '2ncajs8dasm8d');
INSERT INTO users (username, password) VALUES ('admin', 'kl62jdicu31ad');

INSERT INTO notes (userid, title, body) VALUES (-1, 'keep going', 'the next note has the flag!');
INSERT INTO notes (userid, title, body) VALUES (-1, 'your flag', 'Nice work! The flag is flag{r3m3mber_t0-g00gle_wh3n_f@cing_a_d1fficult-challenge!} . Sorry no cowsay in this challenge :( I promise I will somehow make cowsay involved in the next chal');
INSERT INTO notes (userid, title, body) VALUES (-1, 'thats it', 'you dont need to keep reading notes if you dont want to. the flag was one note ago');
