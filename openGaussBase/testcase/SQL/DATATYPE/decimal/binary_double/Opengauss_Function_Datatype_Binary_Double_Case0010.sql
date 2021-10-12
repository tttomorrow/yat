-- @testpoint: 插入字符串类型，合理报错

drop table if exists binary_double10;
create table binary_double10 (name binary_double);
insert into binary_double10 values ('123abc');
insert into binary_double10 values ('111a222');
insert into binary_double10 values ('abc456');
drop table binary_double10;