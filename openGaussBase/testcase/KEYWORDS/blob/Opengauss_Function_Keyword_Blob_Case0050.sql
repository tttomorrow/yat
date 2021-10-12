-- @testpoint: 修改列的数据类型
DROP TABLE IF EXISTS T_BLOB;
CREATE TABLE T_BLOB(ID VARCHAR(100));
INSERT INTO T_BLOB VALUES('35466');
INSERT INTO T_BLOB VALUES('100000');
COMMIT;
ALTER TABLE T_BLOB MODIFY (ID CHAR(150));
ALTER TABLE T_BLOB MODIFY (ID CHAR(50));
ALTER TABLE T_BLOB MODIFY (ID INT);
DROP TABLE IF EXISTS T_BLOB;