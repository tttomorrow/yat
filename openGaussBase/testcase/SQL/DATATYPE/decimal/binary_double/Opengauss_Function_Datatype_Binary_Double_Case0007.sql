-- @testpoint: 插入超出左边界范围值，合理报错

drop table if exists binary_double07;
create table binary_double07 (name binary_double);
insert into binary_double07 values (1.8E-407);
select * from binary_double07;
drop table binary_double07;