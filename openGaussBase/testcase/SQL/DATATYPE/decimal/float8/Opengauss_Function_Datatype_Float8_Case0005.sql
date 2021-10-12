-- @testpoint: 插入左边界范围值

drop table if exists float8_05;
create table float8_05 (name float8);
insert into float8_05 values (1E-307);
select * from float8_05;
drop table float8_05;
