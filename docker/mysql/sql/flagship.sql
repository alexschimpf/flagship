DROP TABLE IF EXISTS flagship.users_projects;
DROP TABLE IF EXISTS flagship.feature_flag_audit_logs;
DROP TABLE IF EXISTS flagship.context_field_audit_logs;
DROP TABLE IF EXISTS flagship.users;
DROP TABLE IF EXISTS flagship.feature_flags;
DROP TABLE IF EXISTS flagship.context_fields;
DROP TABLE IF EXISTS flagship.projects;

CREATE TABLE flagship.projects (
    project_id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL,
    created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (project_id),
    UNIQUE (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE flagship.project_private_keys (
    project_private_key_id INT UNSIGNED AUTO_INCREMENT,
    project_id INT UNSIGNED,
    private_key VARCHAR(184) NOT NULL,
    name VARCHAR(128) NOT NULL,
    created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (project_private_key_id),
    KEY (project_id),
    FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE flagship.feature_flags (
    feature_flag_id INT UNSIGNED AUTO_INCREMENT,
    project_id INT UNSIGNED,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(256) NOT NULL,
    conditions TEXT NOT NULL,
    enabled BOOLEAN DEFAULT 0,
    created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (feature_flag_id),
    KEY (project_id),
    FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE flagship.context_fields (
    context_field_id INT UNSIGNED AUTO_INCREMENT,
    project_id INT UNSIGNED,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(256) NOT NULL,
    field_key VARCHAR(64) NOT NULL,
    value_type TINYINT NOT NULL,
    enum_def TEXT,
    created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (context_field_id),
    KEY (project_id),
    FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE flagship.users (
    user_id INT UNSIGNED AUTO_INCREMENT,
    email VARCHAR(320) NOT NULL,
    name VARCHAR(128) NOT NULL,
    role TINYINT NOT NULL,
    status TINYINT NOT NULL,
    password VARCHAR(200) DEFAULT NULL,
    set_password_token TEXT DEFAULT NULL,
    created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id),
    UNIQUE (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE flagship.users_projects (
    user_id INT UNSIGNED,
    project_id INT UNSIGNED,

    PRIMARY KEY (user_id, project_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,
    FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE flagship.feature_flag_audit_logs (
    audit_log_id INT UNSIGNED AUTO_INCREMENT,
    feature_flag_id INT UNSIGNED,
    project_id INT UNSIGNED,
    actor VARCHAR(320) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(256) NOT NULL,
    conditions TEXT NOT NULL,
    enabled BOOLEAN DEFAULT 0,
    created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (audit_log_id),
    KEY (feature_flag_id),
    KEY (project_id),
    FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE,
    FOREIGN KEY (feature_flag_id)
        REFERENCES feature_flags(feature_flag_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE flagship.context_field_audit_logs (
    audit_log_id INT UNSIGNED AUTO_INCREMENT,
    context_field_id INT UNSIGNED,
    project_id INT UNSIGNED,
    actor VARCHAR(320) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(256) NOT NULL,
    enum_def TEXT,
    created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (audit_log_id),
    KEY (context_field_id),
    KEY (project_id),
    FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON DELETE CASCADE,
    FOREIGN KEY (context_field_id)
        REFERENCES context_fields(context_field_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE flagship.system_audit_logs (
    audit_log_id INT UNSIGNED AUTO_INCREMENT,
    actor VARCHAR(320) NOT NULL,
    event_type INT UNSIGNED NOT NULL,
    details VARCHAR(300) DEFAULT NULL,
    created_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (audit_log_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
