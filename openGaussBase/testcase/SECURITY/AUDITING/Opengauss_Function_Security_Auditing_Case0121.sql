-- @testpoint: 管理员用户给table对象添加多个资源标签，添加成功
--step1: 管理员用户创建table；expect:成功
DROP TABLE IF EXISTS table_security_auditing_0121;
CREATE TABLE table_security_auditing_0121(id int,name char(10));
insert into table_security_auditing_0121 values(1,'lucy');
--step2: 管理员用户给table添加多个资源标签；expect:成功
DROP RESOURCE LABEL IF EXISTS rl01_security_auditing_0121;
DROP RESOURCE LABEL IF EXISTS rl02_security_auditing_0121;
CREATE RESOURCE LABEL rl01_security_auditing_0121 ADD TABLE(table_security_auditing_0121);
CREATE RESOURCE LABEL rl02_security_auditing_0121 ADD TABLE(table_security_auditing_0121);
--step3: 清理环境；expect:成功
DROP RESOURCE LABEL rl01_security_auditing_0121;
DROP RESOURCE LABEL rl02_security_auditing_0121;
DROP TABLE table_security_auditing_0121;
