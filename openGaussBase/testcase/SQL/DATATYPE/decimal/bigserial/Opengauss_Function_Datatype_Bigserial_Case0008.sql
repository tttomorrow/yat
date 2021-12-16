-- @testpoint: 插入右边界范围值

drop table if exists bigserial_08;
create table bigserial_08 (name bigserial);
insert into bigserial_08 values (9223372036854775807);
select * from bigserial_08;
drop table bigserial_08;