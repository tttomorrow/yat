--- Case Type： Comment
--- Case Name： 在列上添加注释

--创建表
drop table if exists comm_test;
create table comm_test(id int,name varchar(10));
insert into comm_test values(1,'a');

--给列添加注释信息
comment on column comm_test.name is '测试列注释添加成功';

--在相关系统表中查看注释是否添加成功
select description from pg_description where objoid=(select tableoid from comm_test);

--清理环境
drop table comm_test;


