--  @testpoint:修改行访问控制策略影响的用户
--创建数据表all_data
drop table if exists all_data cascade;
CREATE TABLE all_data(id int, role varchar(100), data varchar(100));
--创建行访问控制策略，当前用户只能查看用户自身的数据
drop ROW LEVEL SECURITY POLICY if exists all_data_rls ON all_data;
CREATE ROW LEVEL SECURITY POLICY all_data_rls ON all_data USING(role = CURRENT_USER);
--创建用户
drop user if exists test_user1 cascade;
create user test_user1 password 'Xiaxia@123';
--修改行访问控制策略影响的用户
ALTER ROW LEVEL SECURITY POLICY all_data_rls ON all_data TO test_user1;
--删除行访问控制策略
drop ROW LEVEL SECURITY POLICY if exists all_data_rls ON all_data;
--删除表
drop table all_data cascade;
--删除用户
drop user test_user1 cascade;