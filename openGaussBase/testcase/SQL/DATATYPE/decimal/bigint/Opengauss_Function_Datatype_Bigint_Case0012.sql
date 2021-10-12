-- @testpoint: 插入指数形式值

drop table if exists bigint12;
create table bigint12 (name bigint);
insert into bigint12 values (exp(33));
insert into bigint12 values (exp(-15));
insert into bigint12 values (exp(1.0));
insert into bigint12 values (exp(-22.345));
select * from bigint12;
drop table bigint12;