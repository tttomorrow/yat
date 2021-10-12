-- @testpoint: 列存表的表级主键约束，不支持合理报错

DROP TABLE IF EXISTS tab_12;
--ERROR:  column/timeseries store unsupport constraint "PRIMARY KEY"
CREATE TABLE tab_12
(id                     NUMBER(7),
 use_filename              VARCHAR2(20),
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000),
 PRIMARY KEY (id))
 with(ORIENTATION=COLUMN);

 
