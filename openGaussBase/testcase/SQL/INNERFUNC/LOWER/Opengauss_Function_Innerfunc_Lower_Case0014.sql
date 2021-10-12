-- @testpoint: lower函数与group by,having条件联合使用
drop table if exists TEST_LOWER_007;
create table TEST_LOWER_007(COL1 varchar2(20),COL2 int);
insert into TEST_LOWER_007 values ('aHGGFGFaabn',1);
insert into TEST_LOWER_007 values ('aldjfGHJJK',99);
insert into TEST_LOWER_007 values ('aHGGFGFaabn',6);
insert into TEST_LOWER_007 values ('aldjfGHJJK',100);
insert into TEST_LOWER_007 values ('FGGHFfsjds',88);
select lower(COL1),sum(COL2) from TEST_LOWER_007 group by lower(COL1) having lower(COL1) in ('ahggfgfaabn','aldjfghjjk') order by 1,2;
drop table if exists TEST_LOWER_007;