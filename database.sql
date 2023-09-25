drop table if exists users;

create table users (
    id serial,
    email varchar(200) default null,
    username varchar(45) default null,
    first_name varchar(45) default null,
    last_name varchar(45) default null,
    hashed_password varchar(200) default null,
    is_active boolean default null,
    role varchar(45) default null,
    primary key (id)
);

drop table if exists todos;

create table todos (
    id serial,
    title varchar(200) default null,
    description varchar(200) default null,
    priority integer default null,
    primary key (id),
    foreign key (owner_id) references users(id)
);
