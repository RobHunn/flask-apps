create table Users(
    id integer primary key autoincrement,
    name text not null,
    password text not null,
    expert boolean not null,
    admin boolean not null

);

create table Questions(
    id integer primary key autoincrement,
    question text not null,
    answer_text text,
    ask_by_id integer not null,
    expert_id integer not null
)