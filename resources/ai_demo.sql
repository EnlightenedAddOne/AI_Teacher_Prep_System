create database if not exists ai_demo;
use ai_demo;
create table users
(
    id       bigint auto_increment
        primary key,
    username varchar(255)                         not null,
    password varchar(255)                         not null,
    role     enum ('ADMIN', 'TEACHER', 'STUDENT') not null,
    constraint username
        unique (username)
);insert into users (username, password, role) values ('admin', 'admin123', 'ADMIN');

