-- @testpoint: 使用query子句插入来自查询里的数据行
--建表1且插入数据
drop table if exists t_insert02;
create table t_insert02(id int primary key,name varchar(10));
insert into t_insert02 values(1,'Tom'),(2,'lisi');
--建表2
drop table if exists t_insert02_bak;
create table t_insert02_bak(id int primary key,name varchar(10));
--使用insert..query语句给表t_insert02_bak插入数据
insert into t_insert02_bak select * from t_insert02;
--插入id大于5的数据，插入0条数据
insert into t_insert02_bak select * from t_insert02 where id >5;
select * from t_insert02_bak;
--删表
drop table if exists t_insert02;
drop table if exists t_insert02_bak;
