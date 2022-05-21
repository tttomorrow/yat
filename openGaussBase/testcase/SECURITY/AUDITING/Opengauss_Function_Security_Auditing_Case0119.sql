-- @testpoint: 管理员用户给schema对象添加一个资源标签，添加成功
--step1: 管理员用户创建schema；expect:成功
DROP SCHEMA IF EXISTS schema_security_auditing_0119;
CREATE SCHEMA schema_security_auditing_0119;
--step2: 管理员用户给schema添加一个资源标签；expect:成功
DROP RESOURCE LABEL IF EXISTS rl_security_auditing_0119;
CREATE RESOURCE LABEL rl_security_auditing_0119 ADD SCHEMA(schema_security_auditing_0119);
--step3: 清理环境；expect:成功
DROP RESOURCE LABEL rl_security_auditing_0119;
DROP SCHEMA schema_security_auditing_0119;