-- @testpoint: 创建带 PARTIAL CLUSTER KEY 约束的行存表，合理报错

DROP TABLE IF EXISTS tab_12;
CREATE TABLE tab_12
(id                      NUMBER(7),
 use_filename              VARCHAR2(20),
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000),
 PARTIAL CLUSTER KEY (id));
