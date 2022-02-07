DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS data;
DROP TABLE IF EXISTS dataset;
DROP TABLE IF EXISTS inbox;
DROP TABLE IF EXISTS message;


CREATE TABLE user (
    id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    user_name TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE team (
    id TEXT PRIMARY KEY,
    team_name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE role (
    id TEXT PRIMARY KEY,
    role TEXT NOT NULL
);

CREATE TABLE member (
    user_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    role_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (team_id) REFERENCES team (id),
    FOREIGN KEY (role_id) REFERENCES role (id)
);

CREATE TABLE project (
    id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_description TEXT,
    team_id TEXT NOT NULL,
    FOREIGN KEY (team_id) REFERENCES team (id)
);

CREATE TABLE data (
    id TEXT PRIMARY KEY,
    data_name TEXT NOT NULL,
    data_content BLOB NOT NULL,
    data_description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dataset (
    data_id TEXT NOT NULL,
    project_id TEXT NOT NULL,
    role_id TEXT NOT NULL,
    FOREIGN KEY (data_id) REFERENCES data (id),
    FOREIGN KEY (project_id) REFERENCES project (id)
);

CREATE TABLE message (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sender_id TEXT NOT NULL,
    receiver_id TEXT NOT NULL,
    status TEXT DEFAULT 'unread' NOT NULL
);
