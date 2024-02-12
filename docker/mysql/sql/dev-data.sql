INSERT INTO `projects` (`name`, `created_date`, `updated_date`)
VALUES
	('alex', '2024-01-09 01:21:46', '2024-01-09 01:21:46');
INSERT INTO flagship.users_projects (user_id, project_id)
VALUES
    (1, 1);
INSERT INTO `project_private_keys` (`project_id`, `private_key`, `name`)
VALUES
    -- raw private key: 5c18cf7802ac166fcd610c5b7fd24015a417fc110a07dc295e90fd7dce0fd0a3
    (1, 'gAAAAABlyKFJOkSChKo00njI-gPRHdR96V0xcykwHeim2qTJ_IYaQ00kyaDRIXv6r-Rzg2Yi1eXI5ZeCskrcq1WGow51djuyCEhEfcWLaD8amAtIW5EKTxj88Aa5f2yqlUlYryiM3lTJ-5qipYOM-6aWrzp9bC3iLFJ7svGpifl6AtpwnYZuod0=', 'test');
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
