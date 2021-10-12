-- @testpoint: 延迟生效（DEFERRABLE）的唯一约束，使用ON DUPLICATE KEY UPDATE语句，合理报错
--建表,并在事务结束时检查id字段是否有重复
drop table if exists t_insert002;
CREATE TABLE t_insert002(id int unique DEFERRABLE,name varchar(20));
--插入数据,报错ERROR:  INSERT ON DUPLICATE KEY UPDATE does not support deferrable unique constraints/exclusion constraints
insert into t_insert002 values(1,'world'),(1,'hello') ON DUPLICATE KEY UPDATE name = 'newworld';
--删表
drop table t_insert002;