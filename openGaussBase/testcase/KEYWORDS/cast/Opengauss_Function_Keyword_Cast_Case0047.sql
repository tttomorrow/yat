-- @testpoint: 验证cast函数是否支持having条件过滤
drop table if exists TEST_h CASCADE;
create table TEST_h( riqi date);
insert into TEST_h values(to_date('2018-08-15 17:27:39','yyyy-mm-dd hh24:mi:ss'));
insert into TEST_h values(to_date('2018-08-30 17:27:39','yyyy-mm-dd hh24:mi:ss'));
insert into TEST_h values(to_date('2018-09-15 17:27:39','yyyy-mm-dd hh24:mi:ss'));
insert into TEST_h values(to_date('2018-08-16 17:27:39','yyyy-mm-dd hh24:mi:ss'));
insert into TEST_h values(to_date('2018-09-16 17:27:39','yyyy-mm-dd hh24:mi:ss'));
insert into TEST_h values(to_date('2018-08-17 17:27:39','yyyy-mm-dd hh24:mi:ss'));

SELECT COUNT(*) FROM TEST_h T WHERE RIQI<CAST('2018-08-30' AS DATE) GROUP BY RIQI HAVING COUNT(*)>1 ORDER BY
 RIQI DESC;
drop table if exists TEST_h CASCADE;
