-- @testpoint: 对blob类型的主键约束
DROP TABLE IF EXISTS t_blob;
CREATE TABLE t_blob(ID BLOB PRIMARY KEY);
drop table if exists t_blob;