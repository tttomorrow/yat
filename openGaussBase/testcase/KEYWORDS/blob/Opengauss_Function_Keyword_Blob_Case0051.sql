-- @testpoint: BLOB数据类型当表中为空时,修改字段类型为int，合理报错
DROP TABLE IF EXISTS t_blob;
CREATE TABLE t_blob(ID BLOB);
INSERT INTO t_blob VALUES('35466');
INSERT INTO t_blob VALUES('100000');
INSERT INTO t_blob VALUES('C4711A1097876CC');
INSERT INTO t_blob VALUES('');
INSERT INTO t_blob VALUES(NULL);
COMMIT;
ALTER TABLE T_BLOB MODIFY (ID INT);
drop table if exists t_blob;