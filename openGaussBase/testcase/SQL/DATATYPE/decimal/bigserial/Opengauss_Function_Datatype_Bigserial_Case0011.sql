-- @testpoint: 插入指数形式值

drop table if exists bigserial_11;
create table bigserial_11 (name bigserial);
insert into bigserial_11 values (exp(33));
insert into bigserial_11 values (exp(-15));
insert into bigserial_11 values (exp(12.34));
insert into bigserial_11 values (exp(-99.99999));
select * from bigserial_11;
drop table bigserial_11;