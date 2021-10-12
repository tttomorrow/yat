--  @testpoint:修改序列拥有者
--创建序列
drop SEQUENCE if exists serial_c;
CREATE SEQUENCE serial_c INCREMENT by 2 MAXVALUE 5 cycle;
--创建系统管理员用户
drop user if exists test_user1 cascade;
create user test_user1 with sysadmin password 'Xiaxia@123';
--修改序列拥有者（省略if exists）
ALTER SEQUENCE serial_c owner to test_user1;
--添加if exists
ALTER SEQUENCE if exists serial_c owner to test_user1;
--修改不存在的序列，添加if exists，notice提示
ALTER SEQUENCE if exists serial_cafdsfc owner to test_user1;
--修改不存在的序列，省略if exists，合理报错
ALTER SEQUENCE serial_cafdsfc owner to test_user1;
--删除序列
drop SEQUENCE serial_c;
--删除用户
drop user test_user1 cascade;




