-- @testpoint: sin函数与case when的套用

drop table if exists TEST_SIN_01;
create table TEST_SIN_01( COL_1 bigint);
insert into TEST_SIN_01 values(sin(1));

select case when sin(COL_1)>0 then 520 else COL_1 end from TEST_SIN_01;
select case when max(sin(COL_1))>0 then COL_1 else 520 end from TEST_SIN_01 group by col_1;

drop table TEST_SIN_01;