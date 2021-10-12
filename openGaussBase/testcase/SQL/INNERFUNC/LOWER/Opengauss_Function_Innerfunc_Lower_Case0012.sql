-- @testpoint: lower函数作为delete的条件
drop table if exists TEST_LOWER_005;
create table TEST_LOWER_005 (COL1 varchar2(20));
insert into TEST_LOWER_005 values('alshdhggs');
delete from TEST_LOWER_005 where COL1 = lower('ALSHDHGGS');
drop table if exists TEST_LOWER_005;