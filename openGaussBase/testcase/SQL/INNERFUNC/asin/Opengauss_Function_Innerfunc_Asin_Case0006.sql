-- @testpoint: 与关键字结合使用的测试
drop table if exists asin_test_03;
create table asin_test_03( col_1 bigint,col_2 float,col_3 int);
insert into asin_test_03 values(258,0.11022304998774664,10);
SELECT col_1,col_2,col_3 FROM asin_test_03 WHERE col_1 in (asin(0.2323231),asin(0.11),asin(0.102)) order by col_1,col_2,col_3;
SELECT col_1,col_2,col_3 FROM asin_test_03 WHERE COL_1 not in (asin(0.100000),asin(0.110000),asin(0.10200)) order by col_1,col_2,col_3;
drop table if exists asin_test_03;
