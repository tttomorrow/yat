-- @testpoint: WITH子句中，使用INSERT ON DUPLICATE KEY UPDATE语句，合理报错
--建表
drop table if exists t_insert02;
create table t_insert02(id int primary key,name varchar(10));
--with语句使用INSERT ON DUPLICATE KEY UPDATE，合理报错ERROR:  WITH clause is not yet supported whithin INSERT ON DUPLICATE KEY UPDATE statement.
WITH temp_t(id_1,name_1) AS (SELECT id,name FROM t_insert02) insert into t_insert02 values(1,'hello'),(1,'world') ON DUPLICATE KEY UPDATE name = 'hello';
--查询表，未插入数据
select * from t_insert02;
--删除表
drop table t_insert02;
