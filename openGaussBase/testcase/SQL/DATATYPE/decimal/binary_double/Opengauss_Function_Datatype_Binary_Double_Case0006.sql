-- @testpoint: 插入左边界范围值

drop table if exists binary_double06;
create table binary_double06 (name binary_double);
insert into binary_double06 values (1E-307);
select * from binary_double06;
drop table binary_double06;
