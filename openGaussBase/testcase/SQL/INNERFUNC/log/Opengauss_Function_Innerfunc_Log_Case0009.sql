-- @testpoint: log函数嵌套使用
drop table if exists LOG_005;
create table LOG_005(COL_LOG int);
insert into LOG_005 values(log(log(10)));
select COL_LOG as result from LOG_005;
drop table if exists LOG_005;