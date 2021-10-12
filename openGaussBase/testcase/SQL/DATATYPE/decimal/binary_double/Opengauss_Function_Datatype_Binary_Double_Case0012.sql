-- @testpoint: 插入指数形式值

drop table if exists binary_double12;
create table binary_double12 (name binary_double);
insert into binary_double12 values (exp(33));
insert into binary_double12 values (exp(12.34));
insert into binary_double12 values (exp(-15));
insert into binary_double12 values (exp(-0.0012));
select * from binary_double12;
drop table binary_double12;