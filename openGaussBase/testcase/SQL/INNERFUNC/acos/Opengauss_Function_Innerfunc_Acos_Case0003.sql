-- @testpoint: where条件!=,<,>
drop view if exists acos_view;
drop table if exists acos_test_01;
create table acos_test_01(c_decimal decimal(38,4));
insert into acos_test_01(c_decimal) values(-1),(1),(-0.6542),(0.6542),(null);
select c_decimal from acos_test_01 where acos(c_decimal) != 2 and c_decimal is not null order by c_decimal;
select c_decimal from acos_test_01 where acos(c_decimal) > 2 and c_decimal is not null order by c_decimal;
select c_decimal from acos_test_01 where acos(c_decimal) < 2 and c_decimal is not null order by c_decimal;
drop table if exists acos_test_01;
drop view if exists acos_view;
