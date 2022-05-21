-- @testpoint: 同一个审计策略不可同时包含DDL和DML行为,合理报错
--step1: 创建用户,表；expect:成功
drop user if exists u01_security_auditing_0147 cascade;
drop user if exists u02_security_auditing_0147 cascade;
create user u01_security_auditing_0147 password 'Test@123';
create user u02_security_auditing_0147 password 'Test@123';
create table table_security_auditing_0147(id int,name char(10));
--step2: 创建资源标签；expect:成功
drop resource label if exists rl_security_auditing_0147;
create resource label rl_security_auditing_0147 add table(table_security_auditing_0147);
--step3: 创建统一审计策略；expect:失败
drop audit policy if exists audit_security_auditing_0147;
create audit policy audit_security_auditing_0147 privileges analyze, insert, create on label(rl_security_auditing_0147) filter on roles(user001);
--step4: 清理资源；expect:成功
drop resource label if exists rl_security_auditing_0147;
drop table if exists table_security_auditing_0147;
drop user u01_security_auditing_0147 cascade;
drop user u02_security_auditing_0147 cascade;