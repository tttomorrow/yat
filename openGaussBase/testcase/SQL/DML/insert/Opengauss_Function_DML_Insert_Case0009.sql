-- @testpoint: 插入布尔类型，唯一约束列数据重复，合理报错
-- @modify at: 2020-11-16
--建表
DROP TABLE if exists t_bool;
CREATE TABLE t_bool(c1 int,c2 integer,c3 boolean unique);
--插入数据
INSERT INTO t_bool VALUES(1, 10, true);
--再次插入数据，合理报错
insert  into t_bool values(2, 10, true);
--删表
DROP TABLE if exists t_bool;

