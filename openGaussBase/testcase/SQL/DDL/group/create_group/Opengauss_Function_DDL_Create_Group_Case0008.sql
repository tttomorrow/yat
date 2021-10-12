--  @testpoint:创建用户组，CONNECTION LIMIT选项测试
--创建用户组，指定连接数
drop group if exists test_group9;
create group test_group9 with CONNECTION LIMIT -1 PASSWORD 'Xiaxia@123';
--查看用户test_group9设置连接数的限制
SELECT ROLNAME,ROLCONNLIMIT FROM PG_ROLES WHERE ROLNAME='test_group9';
--修改用户test_group9的连接数<-1,合理报错
alter role test_group9 with CONNECTION LIMIT -2;
--删除group
drop group test_group9;