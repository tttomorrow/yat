-- @testpoint: 对blob类型的条件约束
DROP TABLE IF EXISTS t_blob;
CREATE TABLE t_blob(ID BLOB CHECK(ID='100000'));
drop table if exists t_blob;