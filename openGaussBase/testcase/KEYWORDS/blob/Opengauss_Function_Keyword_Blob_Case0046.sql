-- @testpoint: 对blob类型的唯一约束
DROP TABLE IF EXISTS t_blob;
CREATE TABLE t_blob(ID BLOB UNIQUE);
drop table if exists t_blob;