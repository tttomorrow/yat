-- @testpoint: 创建视图
drop view if exists acos_view;
drop table if exists acos_test_01;
create table acos_test_01(c_decimal decimal(38,4));
insert into acos_test_01(c_decimal) values(-1),(1),(-0.6542),(0.6542),(null);
create view acos_view as select acos(c_decimal) t1 from acos_test_01 where c_decimal is not null;
select t1 from acos_view order by t1;
drop view if exists acos_view;
drop table if exists acos_test_01;