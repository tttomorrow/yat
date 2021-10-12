-- @testpoint: 插入指数形式值

drop table if exists int07;
create table int07 (name int);
insert into int07 values (exp(3));
insert into int07 values (exp(0.123));
insert into int07 values (exp(-5));
insert into int07 values (exp(-1.5));
select * from int07;
drop table int07;