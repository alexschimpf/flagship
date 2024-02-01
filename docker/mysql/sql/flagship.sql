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


-- TODO: Clean this up!
INSERT INTO flagship.users (email, name, role, status, password)
VALUES
(
    'owner@flag.ship',
    'Flagship Owner',
    20,
    2,
    '$2a$12$Qwux2dsu.moP5dLszwxJ5uWbPy59UY1PPnoraat/lFh35ZbpZ7SLq' -- Test123!
);
INSERT INTO `projects` (`name`, `created_date`, `updated_date`)
VALUES
	('alex', '2024-01-09 01:21:46', '2024-01-09 01:21:46');
INSERT INTO flagship.users_projects (user_id, project_id)
VALUES
    (1, 1);
INSERT INTO `project_private_keys` (`project_id`, `private_key`, `name`)
VALUES
    (1, 'gAAAAABlnJ-qa9wnux-mAIycDpxqFRGfEbwii3cTtv1a42JDqqncwZk9x131JZGf99ERiSnmTNdMxzDkc5OwQv-BdawEqk408WQeJRSjky-ZXpCtTUKjKuQbjf5N1w1u_HzYAYArGVrEmtsB-HEWqpyv6rI3ZkwinYxVd3ymhuo2kc837sryyck=', 'test');
INSERT INTO `context_fields` (`project_id`, `name`, `description`, `field_key`, `value_type`, `enum_def`, `created_date`, `updated_date`)
VALUES
	(1, 'str', 'str', 'str', 1, NULL, '2024-01-09 01:22:38', '2024-01-09 01:22:38'),
	(1, 'int', 'int', 'int', 3, NULL, '2024-01-09 01:23:03', '2024-01-09 01:23:03');
INSERT INTO `feature_flags` (`project_id`, `name`, `description`, `conditions`, `enabled`, `created_date`, `updated_date`)
VALUES
	(1, 'cde', 'cde', '[[{\"context_key\":\"str\",\"operator\":1,\"value\":\"abc\"}]]', 1, '2024-01-09 01:25:13', '2024-01-09 01:25:13'),
	(1, 'abc', 'abc', '[[{\"context_key\":\"int\",\"operator\":1,\"value\":123}]]', 1, '2024-01-09 01:25:23', '2024-01-09 01:25:23');
INSERT INTO `feature_flag_audit_logs` (`feature_flag_id`, `project_id`, `actor`, `name`, `description`, `conditions`, `enabled`, `created_date`)
VALUES
	(1, 1, 'owner@flag.ship', 'cde', 'cde', '[[{\"context_key\":\"int\",\"operator\":1,\"value\":123}]]', 1, '2024-01-09 01:28:52');
INSERT INTO `context_field_audit_logs` (`context_field_id`, `project_id`, `actor`, `name`, `description`, `enum_def`, `created_date`)
VALUES
	(1, 1, 'owner@flag.ship', 'str', 'str', NULL, '2024-01-09 01:53:53');
INSERT INTO `system_audit_logs` (`actor`, `event_type`, `details`, `created_date`)
VALUES
	('owner@flag.ship', 1, 'whatev', '2024-01-09 02:24:05');
