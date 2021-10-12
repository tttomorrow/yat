-- @testpoint: 插入指数形式值

drop table if exists smallint12;
create table smallint12 (name smallint);
insert into smallint12 values (exp(3));
insert into smallint12 values (exp(1.23));
insert into smallint12 values (exp(-5));
insert into smallint12 values (exp(-1.5));
select * from smallint12;
drop table smallint12;