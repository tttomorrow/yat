-- @testpoint:验证cast函数是否支持having条件过滤
drop table if exists TEST2;   
create table TEST2 (RIQI int);
SELECT T.*,COUNT(*) FROM TEST2 T WHERE RIQI<CAST('2018-08-30' AS DATE) GROUP BY RIQI HAVING COUNT(*)>1 ORDER BY RIQI DESC;
drop table if exists TEST2;