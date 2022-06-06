-- @testpoint: where条件[not] between and,[not] in,[not] null
drop view if exists acos_view;
drop table if exists acos_test_01;
create table acos_test_01(c_decimal decimal(38,4));
insert into acos_test_01(c_decimal) values(-1),(1),(-0.6542),(0.6542),(null);
select c_decimal from acos_test_01 where acos(c_decimal) between 0 and 2 and c_decimal is not null order by c_decimal;
select c_decimal from acos_test_01 where acos(c_decimal) not between 0 and 2 and c_decimal is not null order by c_decimal;
select c_decimal from acos_test_01 where acos(c_decimal) in (3.141592653589793238462643383279502884197,0) and c_decimal is not null order by c_decimal;
select c_decimal from acos_test_01 where acos(c_decimal) not in (3.141592653589793238462643383279502884197,0) and c_decimal is not null order by c_decimal;
select c_decimal from acos_test_01 where acos(c_decimal) is null order by c_decimal;
select c_decimal from acos_test_01 where acos(c_decimal) is not null order by c_decimal;
drop table if exists acos_test_01;
drop view if exists acos_view;
