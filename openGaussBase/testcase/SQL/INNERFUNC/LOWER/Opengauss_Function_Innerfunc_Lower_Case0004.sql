-- @testpoint: lower函数，union all的使用
drop table if exists TEST_LOWER_008;
create table TEST_LOWER_008(COL1 varchar2(20));
insert into TEST_LOWER_008 values ('aHGGFGFaabn');
insert into TEST_LOWER_008 values ('aldjfGHJJK');
insert into TEST_LOWER_008 values ('FGGHFfsjds');
drop table if exists TEST_LOWER_009;
create table TEST_LOWER_009(COL1 varchar2(20));
insert into TEST_LOWER_009 values ('aHGGFGFaabn');
insert into TEST_LOWER_009 values ('asjfGHJKSL');
insert into TEST_LOWER_009 values ('xkcjdjHJKKL');
select lower(COL1) from TEST_LOWER_008 union all select lower(COL1) from TEST_LOWER_009 order by 1;
drop table if exists TEST_LOWER_008;
drop table if exists TEST_LOWER_009;