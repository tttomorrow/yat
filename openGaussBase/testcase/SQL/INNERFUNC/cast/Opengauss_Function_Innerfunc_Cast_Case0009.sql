-- @testpoint:验证cast函数是否支持WHERE条件查询
drop table if exists TEST2;   
create table TEST2 (RIQI int);
SELECT * FROM TEST2 WHERE RIQI>CAST('2018-08-30' AS DATE);
drop table if exists TEST2;