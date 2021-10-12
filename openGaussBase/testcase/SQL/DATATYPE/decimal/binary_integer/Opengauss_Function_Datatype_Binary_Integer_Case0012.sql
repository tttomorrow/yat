-- @testpoint: 插入浮点数，四舍五入

drop table if exists binary_integer12;
create table binary_integer12 (name binary_integer);
insert into binary_integer12 values (122.3340);
insert into binary_integer12 values (0.0000123);
insert into binary_integer12 values (-122.3340);
insert into binary_integer12 values (-0.0000123);
select * from binary_integer12;
drop table binary_integer12;