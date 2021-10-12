-- @testpoint: 插入数据类型系统无法进行转换，合理报错
--建表
drop table if exists t_insert;
create table t_insert(c_insert1 char(20),c_insert2 bit varying(10));
--插入数据与类型匹配，成功
insert into t_insert values('hello',B'101');
--插入数据与类型不匹配，失败
insert into t_insert values(20,101);
--查询表
select * from t_insert;
--删表
drop table t_insert;