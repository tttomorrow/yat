-- @testpoint: 插入指数形式值

drop table if exists float8_11;
create table float8_11 (name float8);
insert into float8_11 values (exp(33));
insert into float8_11 values (exp(12.34));
insert into float8_11 values (exp(-15));
insert into float8_11 values (exp(-12.34));
select * from float8_11;
drop table float8_11;