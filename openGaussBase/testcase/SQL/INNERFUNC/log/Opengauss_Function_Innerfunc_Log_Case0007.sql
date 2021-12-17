-- @testpoint: log函数入参给double precision类型
drop table if exists LOG_003;
create table LOG_003(COL_LOG double precision);
insert into LOG_003 values(100.0000000000004);
insert into LOG_003 values(99.99999999999999);
select log(COL_LOG) as RESULT from LOG_003 order by COL_LOG;
drop table if exists LOG_003;