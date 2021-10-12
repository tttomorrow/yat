-- @testpoint: 插入左边界范围值

drop table if exists float05;
create table float05 (name float);
insert into float05 values (1E-307);
select * from float05;
drop table float05;
