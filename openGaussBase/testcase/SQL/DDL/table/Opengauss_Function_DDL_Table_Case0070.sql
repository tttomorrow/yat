-- @testpoint: create table与 with 子句（DELTAROW_THRESHOLD）该参数只对列存表有效。

DROP TABLE IF EXISTS tab_17;
CREATE TABLE tab_17
(id               NUMBER(7),
 name              VARCHAR2(20)
  )with(ORIENTATION=COLUMN,DELTAROW_THRESHOLD=1999);
DROP TABLE IF EXISTS tab_17;














 
