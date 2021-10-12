-- @testpoint: 创建带 唯一约束的行存表字段约束，合理报错
DROP TABLE IF EXISTS tab_12;
-- 列/时序存储不支持约束"UNIQUE"
CREATE TABLE tab_12
(id                     NUMBER(7) UNIQUE,
 use_filename              VARCHAR2(20),
 filename                  VARCHAR2(255),
 text                       VARCHAR2(2000)
 )
with(ORIENTATION=COLUMN);

