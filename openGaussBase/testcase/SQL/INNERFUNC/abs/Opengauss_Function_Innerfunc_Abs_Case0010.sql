-- @testpoint: 输入参数为字段表达式
drop table if exists abs_test_04;
create table abs_test_04 (F1 INT,F2 INT);
insert into abs_test_04 values (-99,20);
select abs(a.F1+a.F2) from abs_test_04 as a where F1=-99;
drop table if exists abs_test_04;