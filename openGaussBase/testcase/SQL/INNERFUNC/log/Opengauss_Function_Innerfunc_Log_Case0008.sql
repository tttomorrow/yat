-- @testpoint: log函数入参给numeric类型
drop table if exists LOG_004;
create table LOG_004(COL_LOG numeric);
insert into LOG_004 values(100.0);
select log(COL_LOG) as RESULT from LOG_004;
drop table if exists LOG_004;