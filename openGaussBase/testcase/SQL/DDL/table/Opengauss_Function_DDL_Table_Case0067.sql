-- @testpoint: create table与 with 子句（COMPRESSLEVEL）
DROP TABLE IF EXISTS tab_16;
CREATE TABLE tab_16
(id                      NUMBER(7),
 name              VARCHAR2(20)
  )with(ORIENTATION=COLUMN,COMPRESSION=HIGH,COMPRESSLEVEL=2);
DROP TABLE IF EXISTS tab_16;