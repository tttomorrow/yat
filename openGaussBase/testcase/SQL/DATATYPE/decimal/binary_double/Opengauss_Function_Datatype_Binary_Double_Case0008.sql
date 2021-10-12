-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists binary_double08;
create table binary_double08 (name binary_double);
insert into binary_double08 values (1.8E+308);
select * from binary_double08;
drop table binary_double08;
