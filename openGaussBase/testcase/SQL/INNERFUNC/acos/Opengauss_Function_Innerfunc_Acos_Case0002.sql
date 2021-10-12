--  @testpoint:distinct的使用

drop view if exists acos_view;
drop table if exists acos_test_01;
create table acos_test_01(c_decimal decimal(38,4));
insert into acos_test_01(c_decimal) values(-1),(1),(-0.6542),(0.6542),(null);

select distinct acos(abs(c_decimal)) t1,acos(abs(c_decimal)) t2 from acos_test_01 where c_decimal is not null order by t1,t2;
drop table if exists acos_test_01;
drop view if exists acos_view;