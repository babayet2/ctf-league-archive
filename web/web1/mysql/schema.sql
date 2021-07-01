CREATE DATABASE web1;
USE web1;

CREATE TABLE `users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(500) NOT NULL,
    `password` VARCHAR(500) NOT NULL,
    KEY `id` (`id`) USING BTREE,
    PRIMARY KEY (`id`)
);

INSERT INTO users (username, password) VALUES ('aaron', 'i use arch btw');
INSERT INTO users (username, password) VALUES ('hadi', 'this is hadi''s personal backdoor account');
INSERT INTO users (username, password) VALUES ('zander', '??????????? password hashing??????????????');
INSERT INTO users (username, password) VALUES ('lance', 'I CAN CARRY YOUR CRYPTOOOOO');
INSERT INTO users (username, password) VALUES ('admin', 'pacman -Syu');

