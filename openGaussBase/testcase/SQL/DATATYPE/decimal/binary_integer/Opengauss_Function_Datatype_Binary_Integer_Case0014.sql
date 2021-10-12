-- @testpoint: 非空binary_integer类型插入空值,合理报错

drop table if exists binary_integer14;
create table binary_integer14 (name binary_integer,name2 binary_integer not null);
insert into binary_integer14 values (122,'');
drop table binary_integer14;