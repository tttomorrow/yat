-- @testpoint: 创建视图，结合使用测试
drop view if exists asin_view_test_01;
drop view if exists asin_view_test_02;
drop table if exists asin_test_04;
create table asin_test_04( col_1 bigint,col_2 float,col_3 int);
insert into asin_test_04 values(258,0.11022304998774664,10);
drop view if exists asin_view_test_01;
drop view if exists asin_view_test_02;
create view asin_view_test_01 as select col_1,col_2,col_3 from asin_test_04
where exists(SELECT col_1,col_2,col_3 from asin_test_04 where COL_1 not in (ASIN(0.1),ASIN(0.11),ASIN(0.102)));
create view asin_view_test_02 as select col_1,col_2,col_3 from asin_test_04 where COL_1 in (ASIN(0.1),ASIN(0.11),ASIN(0.102));
drop view if exists asin_view_test_02;
drop view if exists asin_view_test_01;
drop table if exists asin_test_04;