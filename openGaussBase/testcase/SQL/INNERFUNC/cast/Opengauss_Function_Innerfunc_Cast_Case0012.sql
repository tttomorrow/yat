-- @testpoint: 验证cast函数是否支持伪列
-- @modify at: 2020-11-16
drop table if exists TEST2;   
create table TEST2 (RIQI int);
insert into TEST2 values(1),(2),(9);
select ROWNUM from TEST2;
drop table if exists TEST2;