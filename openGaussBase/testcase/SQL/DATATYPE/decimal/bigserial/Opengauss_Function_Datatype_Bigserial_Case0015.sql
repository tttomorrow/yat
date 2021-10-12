-- @testpoint: 插入default自定义值

drop table if exists bigserial_15;
create table bigserial_15 (name bigserial);
insert into bigserial_15 values (default);
insert into bigserial_15 values (default);
insert into bigserial_15 values (default);
insert into bigserial_15 values (default);
insert into bigserial_15 values (default);
select * from bigserial_15;
drop table bigserial_15;