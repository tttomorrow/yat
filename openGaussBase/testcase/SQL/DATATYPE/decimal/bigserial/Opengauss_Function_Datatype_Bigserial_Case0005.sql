-- @testpoint: 插入左边界范围值

drop table if exists bigserial_05;
create table bigserial_05 (name bigserial);
insert into bigserial_05 values (1);
select * from bigserial_05;
drop table  bigserial_05;