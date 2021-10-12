--  @testpoint:与insert into结合的边界值使用

drop view if exists acos_view;
drop table if exists acos_test_01;
create table acos_test_01(c_decimal decimal(38,4));
insert into acos_test_01(c_decimal) values(-1),(1),(-0.6542),(0.6542),(null);

select acos(c_decimal) t1 from acos_test_01 where c_decimal in (1,-1) order by t1;
drop table if exists acos_test_01;
drop view if exists acos_view;