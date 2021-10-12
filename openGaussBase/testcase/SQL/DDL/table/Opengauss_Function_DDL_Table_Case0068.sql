-- @testpoint: create table和 with 子句（MAX_BATCHROW）联合使用，该参数只对列存表有效。
DROP TABLE IF EXISTS tab_17;
CREATE TABLE tab_17
(id               NUMBER(7),
 name              VARCHAR2(20)
  )with(ORIENTATION=COLUMN,MAX_BATCHROW=20000);
DROP TABLE IF EXISTS tab_17;