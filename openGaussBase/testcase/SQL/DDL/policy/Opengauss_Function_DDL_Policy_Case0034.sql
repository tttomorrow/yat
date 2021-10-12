--  @testpoint:同一张表创建101个行访问控制策略，合理报错
drop table if exists test_policy_002 cascade;
create table test_policy_002(id int,usr name);
--打开行级安全检查
ALTER TABLE test_policy_002 ENABLE ROW LEVEL SECURITY;
--创建测试用户
drop user if exists s_usr1 cascade;
create user s_usr1 password 'Test@123';
--授予用户表的select权限
grant select on test_policy_002 to s_usr1;
--创建策略,指定行访问控制影响的数据库用户为public
drop POLICY if exists t_pol_ ON test_policy_002;
--创建存储过程，执行创建策略101次,合理报错
create or replace procedure create_policy1()
as
begin
	for i in 1..101 loop
		execute immediate 'CREATE POLICY t_pol_'|| i || ' ON test_policy_002 FOR SELECT TO PUBLIC USING (usr = current_user);';
	end loop;
end;
/
--调用存储过程
call create_policy1();
--删除存储过程
drop procedure if exists create_policy1;
--删除表
drop table if exists test_policy_002 cascade;
--删除用户
drop user if exists s_usr1 cascade;