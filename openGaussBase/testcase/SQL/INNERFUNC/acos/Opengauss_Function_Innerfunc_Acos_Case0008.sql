--  @testpoint:函数嵌套使用

drop table if exists acos_test_04;
create table acos_test_04(COL_ACOS INTEGER);
insert into acos_test_04 values(0);
insert into acos_test_04 values(1);
select cast(ACOS(COL_ACOS)as numeric(3,2)) as RESULT from acos_test_04;
drop table if exists acos_test_04;
