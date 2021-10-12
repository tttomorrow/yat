-- @testpoint: 给同一个表多次添加注释，结果会覆盖之前的注释信息，以最后一次为主


--创建表
drop table if exists table_comment;
create table table_comment(id int);

--给表多次添加注释信息
comment on table table_comment is '测试表注释添加成功1';
comment on table table_comment is '测试表注释添加成功2';
comment on table table_comment is '测试表注释添加成功3';
comment on table table_comment is '测试表注释添加成功4';
comment on table table_comment is '测试表注释添加成功5';

--在相关系统表中查看注释是否添加成功
--表的注释为最后一次添加的信息
select description from pg_description where objoid=(select relid from pg_stat_all_tables where relname = 'table_comment');

--清理环境
drop table table_comment;


