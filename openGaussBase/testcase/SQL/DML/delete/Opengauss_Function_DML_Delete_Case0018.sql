--  @testpoint:删除临时表数据
--创建临时表
create temp table tmp_test1 (id int,name varchar(20));
insert into tmp_test1 values(1,'李丽'),(2,'李小丽');
--删除表
delete from tmp_test1;
--创建临时表
drop table if exists tmp_test1;
create temp table tmp_test1 (id int,name varchar(20));
insert into tmp_test1 values(1,'李丽'),(2,'李小丽');
--删除临时表数据
delete from tmp_test1;
--删除表
drop table if exists tmp_test1;