create table users
(
    user_id       int auto_increment
        primary key,
    username      varchar(50)          not null,
    password_hash varchar(255)         not null,
    email         varchar(100)         not null,
    role          varchar(20)          not null,
    wrong_attempt int        default 0 null,
    is_locked     tinyint(1) default 0 null,
    constraint email
        unique (email),
    constraint username
        unique (username)
);

create table clients
(
    user_id       int                         not null
        primary key,
    company_name  varchar(100)                not null,
    budget        decimal(10, 2) default 0.00 null,
    average_grade decimal(3, 2)  default 0.00 null,
    constraint clients_ibfk_1
        foreign key (user_id) references users (user_id)
            on delete cascade
);

create table conversation_threads
(
    thread_id     int auto_increment
        primary key,
    client_id     int                                 not null,
    freelancer_id int                                 not null,
    subject       varchar(255)                        null,
    created_at    timestamp default CURRENT_TIMESTAMP null,
    updated_at    timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    constraint client_id
        unique (client_id, freelancer_id),
    constraint fk_thread_client
        foreign key (client_id) references users (user_id)
            on delete cascade,
    constraint fk_thread_freelancer
        foreign key (freelancer_id) references users (user_id)
            on delete cascade
);

create table freelancer_history
(
    history_id int auto_increment
        primary key,
    user_id    int            not null,
    job_title  varchar(100)   not null,
    earnings   decimal(10, 2) not null,
    constraint freelancer_history_ibfk_1
        foreign key (user_id) references users (user_id)
            on delete cascade
);

create index user_id
    on freelancer_history (user_id);

create table freelancer_languages
(
    language_id   int auto_increment
        primary key,
    user_id       int         not null,
    language_name varchar(50) not null,
    constraint user_id
        unique (user_id, language_name),
    constraint freelancer_languages_ibfk_1
        foreign key (user_id) references users (user_id)
            on delete cascade
);

create table freelancer_portfolio
(
    portfolio_id int auto_increment
        primary key,
    user_id      int          not null,
    link_url     varchar(255) not null,
    constraint freelancer_portfolio_ibfk_1
        foreign key (user_id) references users (user_id)
            on delete cascade
);

create index user_id
    on freelancer_portfolio (user_id);

create table freelancer_skills
(
    skill_id   int auto_increment
        primary key,
    user_id    int         not null,
    skill_name varchar(50) not null,
    constraint user_id
        unique (user_id, skill_name),
    constraint freelancer_skills_ibfk_1
        foreign key (user_id) references users (user_id)
            on delete cascade
);

create table freelancers
(
    user_id             int                        not null
        primary key,
    name                varchar(100)               not null,
    years_of_experience int           default 0    null,
    rating              decimal(3, 2) default 0.00 null,
    constraint freelancers_ibfk_1
        foreign key (user_id) references users (user_id)
            on delete cascade
);

create table jobs
(
    job_id      int auto_increment
        primary key,
    client_id   int                          not null,
    title       varchar(255)                 not null,
    description text                         not null,
    budget      decimal(10, 2)               not null,
    deadline    date                         not null,
    seniority   varchar(50) default 'Junior' null,
    status      varchar(20) default 'Open'   null,
    constraint jobs_ibfk_1
        foreign key (client_id) references users (user_id)
            on delete cascade
);

create table applications
(
    application_id    int auto_increment
        primary key,
    job_id            int                                 not null,
    freelancer_id     int                                 not null,
    cover_letter      text                                not null,
    proposed_price    decimal(10, 2)                      not null,
    proposed_deadline int                                 not null,
    created_at        timestamp default CURRENT_TIMESTAMP null,
    constraint unique_application
        unique (job_id, freelancer_id),
    constraint applications_freelancer_fk
        foreign key (freelancer_id) references freelancers (user_id)
            on delete cascade,
    constraint applications_job_fk
        foreign key (job_id) references jobs (job_id)
            on delete cascade
);

create index client_id
    on jobs (client_id);

create table messages
(
    message_id int auto_increment
        primary key,
    thread_id  int                                 not null,
    sender_id  int                                 not null,
    body       text                                not null,
    created_at timestamp default CURRENT_TIMESTAMP null,
    constraint fk_msg_sender
        foreign key (sender_id) references users (user_id)
            on delete cascade,
    constraint fk_msg_thread
        foreign key (thread_id) references conversation_threads (thread_id)
            on delete cascade
);

create table thread_participants
(
    thread_id    int                                  not null,
    user_id      int                                  not null,
    is_archived  tinyint(1) default 0                 null,
    last_read_at timestamp  default CURRENT_TIMESTAMP null,
    primary key (thread_id, user_id),
    constraint fk_part_thread
        foreign key (thread_id) references conversation_threads (thread_id)
            on delete cascade,
    constraint fk_part_user
        foreign key (user_id) references users (user_id)
            on delete cascade
);

