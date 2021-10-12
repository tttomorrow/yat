-- @testpoint: lower函数作为join条件
drop table if exists TEST_LOWER_005;
create table TEST_LOWER_005 (COL1 varchar2(20));
insert into TEST_LOWER_005 values('ABCDEF');
drop table if exists TEST_LOWER_006;
create table TEST_LOWER_006 (COL1 varchar2(20));
insert into TEST_LOWER_006 values('ABCDEF');
select a.COL1 from TEST_LOWER_005 a inner join TEST_LOWER_006 b on lower(a.COL1)=lower(b.COL1) order by 1;
drop table if exists TEST_LOWER_005;
drop table if exists TEST_LOWER_006;