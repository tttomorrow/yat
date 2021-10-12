--  @testpoint:使用delete删除表，表名分别使用table_name和table_name*
--建表
drop table if exists test_1t cascade;
create table test_1t (id int,name varchar(20));
--插入数据
insert into test_1t values(generate_series(1,100),'liyu');
--删除表中所有数据
delete from test_1t;
--查询表信息，表中数据为空
select * from test_1t;
--通过系统表查询删除行数
select n_tup_del from  pg_stat_all_tables where relname = 'test_1t';
--建表
drop table if exists test_2t cascade;
create table test_2t (id int,name varchar(20));
--插入数据
insert into test_2t values(generate_series(1,100),'liyu');
--删除表中所有数据
delete from test_2t*;
--查询表信息，表中数据为空
select * from test_2t;
--通过系统表查询删除行数
select n_tup_del from  pg_stat_all_tables where relname = 'test_2t';
--删除表
drop table test_1t;
drop table test_2t;
--删除不存在的表，合理报错
delete from test_1t;

