--- Case Type： Comment
--- Case Name： 在表上添加注释

--创建表
drop table if exists comm_test;
create table comm_test(id int);

--给表添加注释信息
comment on table comm_test is '测试表注释添加成功';

--在相关系统表中查看注释是否添加成功
select description from pg_description where objoid=(select relid from pg_stat_all_tables where relname = 'comm_test');

--清理环境
drop table comm_test;


