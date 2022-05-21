-- @testpoint: 管理员用户给view对象添加1个资源标签，添加成功
--step1: 管理员用户创建view；expect:成功
DROP VIEW IF EXISTS v_security_auditing_0123;
CREATE VIEW v_security_auditing_0123 AS SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
--step2: 管理员用户给view添加多个资源标签；expect:成功
DROP RESOURCE LABEL IF EXISTS rl_security_auditing_0123;
CREATE RESOURCE LABEL rl_security_auditing_0123 ADD VIEW(v_security_auditing_0123);
--step3: 清理环境；expect:成功
DROP RESOURCE LABEL rl_security_auditing_0123;
DROP VIEW v_security_auditing_0123;