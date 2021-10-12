-- @testpoint: BLOB数据类型设置为NULL
DROP TABLE if exists t_blob;
CREATE TABLE t_blob(ID blob);
alter table t_blob modify ID null;
INSERT INTO t_blob VALUES('35466');
INSERT INTO t_blob VALUES('100000');
INSERT INTO t_blob VALUES('C4711A1097876CC');
INSERT INTO t_blob VALUES('');
INSERT INTO t_blob VALUES(NULL);
drop table if exists t_blob;