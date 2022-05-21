-- @testpoint: 管理员用户给view对象添加多个资源标签，添加成功
--step1: 管理员用户创建view；expect:成功
DROP VIEW IF EXISTS v_security_auditing_0124;
CREATE VIEW v_security_auditing_0124 AS SELECT * FROM pg_tablespace WHERE spcname = 'pg_default';
--step2: 管理员用户给view添加多个资源标签；expect:成功
DROP RESOURCE LABEL IF EXISTS rl01_security_auditing_0124;
DROP RESOURCE LABEL IF EXISTS rl02_security_auditing_0124;
CREATE RESOURCE LABEL rl01_security_auditing_0124 ADD VIEW(v_security_auditing_0124);
CREATE RESOURCE LABEL rl02_security_auditing_0124 ADD VIEW(v_security_auditing_0124);
--step3: 清理环境；expect:成功
DROP RESOURCE LABEL rl01_security_auditing_0124;
DROP RESOURCE LABEL rl02_security_auditing_0124;
DROP VIEW v_security_auditing_0124;