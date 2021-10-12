-- @testpoint: log(b numeric, x numeric)函数合法值测试
drop table if exists LOG_006;
create table LOG_006(COL_LOG_B numeric, COL_LOG_X numeric);
insert into LOG_006 values(log(2,8), log(2.0,8.0));
select COL_LOG_B as RESULT1,COL_LOG_X as RESULT2 from LOG_006;
drop table if exists LOG_006;