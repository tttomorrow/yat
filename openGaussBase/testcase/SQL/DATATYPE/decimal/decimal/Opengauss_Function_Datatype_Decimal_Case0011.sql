-- @testpoint: 插入指数形式值

drop table if exists decimal_11;
create table decimal_11 (name decimal);
insert into decimal_11 values (exp(33));
insert into decimal_11 values (exp(12.34));
insert into decimal_11 values (exp(-15));
insert into decimal_11 values (exp(-12.34));
select * from decimal_11;
drop table decimal_11;