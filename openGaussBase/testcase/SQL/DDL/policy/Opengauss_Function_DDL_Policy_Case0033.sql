--  @testpoint:同一张表最多创建100个行访问控制策略
drop table if exists test_policy_001 cascade;
create table test_policy_001(id int,usr name);
--打开行级安全检查
ALTER TABLE test_policy_001 ENABLE ROW LEVEL SECURITY;
--创建测试用户
drop user if exists s_usr1 cascade;
create user s_usr1 password 'Test@123';
--授予用户表的select权限
grant select on test_policy_001 to s_usr1;
--创建策略,指定行访问控制影响的数据库用户为public
drop POLICY if exists t_pol_ ON test_policy_001;
--创建存储过程，执行创建策略100次
create or replace procedure create_policy()
as
begin
	for i in 1..100 loop
		execute immediate 'CREATE POLICY t_pol_'|| i || ' ON test_policy_001 FOR SELECT TO PUBLIC USING (usr = current_user);';
	end loop;
end;
/
--调用存储过程
call create_policy();
--验证test_policy_001表有100个策略名
select count(*) from pg_rlspolicy where polname like 't_pol_%' and polrelid = (select oid from pg_class where relname = 'test_policy_001');
--删除策略
create or replace procedure drop_policy()
as
begin
	for i in 1..100 loop
		execute immediate 'DROP POLICY t_pol_'|| i || ' ON test_policy_001 ;';
	end loop;
end;
/
--调用存储过程
call drop_policy();
--删除存储过程
drop procedure if exists create_policy;
drop procedure if exists drop_policy;
--删除表
drop table if exists test_policy_001 cascade;
--删除用户
drop user if exists s_usr1 cascade;



