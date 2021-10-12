-- @testpoint: 插入bool类型，合理报错

drop table if exists binary_double11;
create table binary_double11 (name binary_double);
insert into binary_double11 values (true);
insert into binary_double11 values (false);
select * from binary_double11;
drop table binary_double11;