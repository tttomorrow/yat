--  @testpoint:输入参数为无效值(合理报错)


drop table if exists acos_test_05;
create table acos_test_05(COL_ACOS double precision);
insert into acos_test_05 VALUES(1.23);
insert into acos_test_05 VALUES(-1.23);

SELECT ACOS(COL_ACOS) AS RESULT FROM acos_test_05 WHERE COL_ACOS=1.23;
SELECT ACOS(COL_ACOS) AS RESULT FROM acos_test_05 WHERE COL_ACOS=-1.23;
drop table if exists acos_test_05;