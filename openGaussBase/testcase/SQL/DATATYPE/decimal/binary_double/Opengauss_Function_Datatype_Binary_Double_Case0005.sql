-- @testpoint: 插入特殊字符,合理报错

drop table if exists binary_double05;
create table binary_double05 (name binary_double);
insert into binary_double05 values (!@#$%^&*);
drop table binary_double05;