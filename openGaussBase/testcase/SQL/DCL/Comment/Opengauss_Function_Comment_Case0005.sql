--- Case Type： Comment
--- Case Name： 在数据库上添加注释

--创建数据库
drop database if exists database_comment;
create database database_comment;

--给数据库添加注释信息
comment on database database_comment is '测试数据库注释添加成功';

--在相关系统表中查看注释是否添加成功
select description from pg_shdescription where objoid=(select oid from pg_database where datname='database_comment');

--清理环境
drop database database_comment;


