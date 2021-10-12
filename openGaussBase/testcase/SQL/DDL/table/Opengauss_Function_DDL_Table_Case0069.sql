-- @testpoint:  create table与 with 子句（PARTIAL_CLUSTER_ROWS）该参数只对列存表有效。

DROP TABLE IF EXISTS tab_17;
CREATE TABLE tab_17
(id               NUMBER(7),
 name              VARCHAR2(20)
  )with(ORIENTATION=COLUMN,PARTIAL_CLUSTER_ROWS=2000000);
DROP TABLE IF EXISTS tab_17;