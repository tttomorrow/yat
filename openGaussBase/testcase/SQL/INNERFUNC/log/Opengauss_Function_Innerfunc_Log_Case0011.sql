-- @testpoint: log函数入参为表达式
drop table if exists LOG_007;
create table LOG_007(COL_LOG_B numeric, COL_LOG_X numeric);
insert into LOG_007 values(log(log(1+2*6/4-2+ |/4, 64*4), ||/8));
select COL_LOG_B as RESULT from LOG_007;
drop table if exists LOG_007;