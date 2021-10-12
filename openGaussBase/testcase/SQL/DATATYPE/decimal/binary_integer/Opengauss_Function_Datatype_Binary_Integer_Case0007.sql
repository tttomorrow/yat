-- @testpoint: 插入指数形式值

drop table if exists binary_integer07;
create table binary_integer07 (name binary_integer);
insert into binary_integer07 values (exp(3));
insert into binary_integer07 values (exp(3.222));
insert into binary_integer07 values (exp(-5));
insert into binary_integer07 values (exp(-0.112));
select * from binary_integer07;
drop table binary_integer07;