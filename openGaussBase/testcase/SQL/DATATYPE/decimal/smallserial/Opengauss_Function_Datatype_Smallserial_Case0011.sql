-- @testpoint: 插入指数形式值

drop table if exists smallserial_11;
create table smallserial_11 (name smallserial);
insert into smallserial_11 values (exp(2));
insert into smallserial_11 values (exp(1.23));
insert into smallserial_11 values (exp(-15));
insert into smallserial_11 values (exp(-1.5));
select * from smallserial_11;
drop table smallserial_11;