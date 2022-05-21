-- @testpoint: 管理员用户给function对象添加多个资源标签，添加成功
--step1: 管理员用户创建function；expect:成功
DROP FUNCTION IF EXISTS func_security_auditing_0125;
CREATE FUNCTION func_security_auditing_0125(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
--step2: 管理员用户给function添加多个资源标签；expect:成功
DROP RESOURCE LABEL IF EXISTS rl01_security_auditing_0125;
DROP RESOURCE LABEL IF EXISTS rl02_security_auditing_0125;
CREATE RESOURCE LABEL rl01_security_auditing_0125 ADD FUNCTION(func_security_auditing_0125);
CREATE RESOURCE LABEL rl02_security_auditing_0125 ADD FUNCTION(func_security_auditing_0125);
--step3: 清理环境；expect:成功
DROP RESOURCE LABEL rl01_security_auditing_0125;
DROP RESOURCE LABEL rl02_security_auditing_0125;
DROP FUNCTION func_security_auditing_0125;