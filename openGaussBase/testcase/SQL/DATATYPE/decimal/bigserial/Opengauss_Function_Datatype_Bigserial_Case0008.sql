-- @testpoint: 插入右边界范围值

drop table if exists bigserial_08;
create table bigserial_08 (name bigserial);
select * from bigserial_08;
drop table bigserial_08;