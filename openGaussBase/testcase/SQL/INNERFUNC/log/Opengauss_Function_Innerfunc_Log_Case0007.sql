-- @testpoint: log函数入参给double precision类型
drop table if exists LOG_003;
create table LOG_003(COL_LOG double precision);
select log(COL_LOG) as RESULT from LOG_003 order by COL_LOG;
drop table if exists LOG_003;