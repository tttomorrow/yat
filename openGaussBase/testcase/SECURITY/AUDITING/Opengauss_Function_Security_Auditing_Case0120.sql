-- @testpoint: 管理员用户给schema对象添加多个资源标签，添加成功
--step1: 管理员用户创建schema；expect:成功
DROP SCHEMA IF EXISTS schema_security_auditing_0120;
CREATE SCHEMA schema_security_auditing_0120;
--step2: 管理员用户给schema添加多个资源标签；expect:成功
DROP RESOURCE LABEL IF EXISTS rl01_security_auditing_0120;
DROP RESOURCE LABEL IF EXISTS rl02_security_auditing_0120;
CREATE RESOURCE LABEL rl01_security_auditing_0120 ADD SCHEMA(schema_security_auditing_0120);
CREATE RESOURCE LABEL rl02_security_auditing_0120 ADD SCHEMA(schema_security_auditing_0120);
--step3: 清理环境；expect:成功
DROP RESOURCE LABEL rl01_security_auditing_0120;
DROP RESOURCE LABEL rl02_security_auditing_0120;
DROP SCHEMA schema_security_auditing_0120;