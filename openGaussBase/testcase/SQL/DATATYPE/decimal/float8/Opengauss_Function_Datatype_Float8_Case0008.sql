-- @testpoint: 插入右边界范围值

drop table if exists float06;
create table float06 (name float8);
insert into float06 values (1E+308);
select * from float06;
drop table float06;
