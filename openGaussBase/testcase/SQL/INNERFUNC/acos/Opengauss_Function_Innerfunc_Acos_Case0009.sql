--  @testpoint:输入参数为null，''

drop table if exists acos_test_06;
create table acos_test_06(COL_ACOS double precision);
insert into acos_test_06 values(null);
insert into acos_test_06 values('');

select ACOS(COL_ACOS) as RESULT from acos_test_06;
select ACOS(COL_ACOS) as RESULT from acos_test_06;
drop table if exists acos_test_06;


