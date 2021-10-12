--- Case Type： Comment
--- Case Name： 在表上添加注释,再清空掉注释

--创建表
drop table if exists table_comment;
create table table_comment(id int);

--给表添加注释信息
comment on table table_comment is '测试表注释添加成功';

--在相关系统表中查看注释是否添加成功
select description from pg_description where objoid=(select relid from pg_stat_all_tables where relname = 'table_comment');

--清空表添加的注释
comment on table table_comment is '';

--在相关系统表中查看注释是否清除成功
select description from pg_description where objoid=(select relid from pg_stat_all_tables where relname = 'table_comment');

--清理环境
drop table table_comment;


