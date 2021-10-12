--  @testpoint:openGauss关键字temporary(非保留)
-- 创建全局临时表，并指定会话结束时删除该临时表数据
DROP TABLE  IF EXISTS table_test3;
CREATE GLOBAL TEMPORARY TABLE table_test3 ( ID INTEGER NOT NULL, NAME CHAR(16) NOT NULL, ADDRESS VARCHAR(50) , POSTCODE CHAR(6) ) ON COMMIT PRESERVE ROWS;
DROP TABLE  table_test3;