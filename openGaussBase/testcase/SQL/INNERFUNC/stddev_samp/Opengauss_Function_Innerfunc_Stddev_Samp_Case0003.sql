-- @testpoint: 入参为bool类型的列，分组求标准差
drop table if exists test1;
create table test1(col_1 BOOLEAN, col_2 BOOLEAN);
insert into test1 values(true,false);
insert into test1 values('t','f');
insert into test1 values(1,0);
select STDDEV_SAMP(COL_1),STDDEV_SAMP(COL_2) from test1;
drop table if exists test1;