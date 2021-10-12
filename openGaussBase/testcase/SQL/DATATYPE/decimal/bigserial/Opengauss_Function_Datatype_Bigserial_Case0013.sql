-- @testpoint: 插入0值

drop table if exists bigserial_13;
create table bigserial_13 (name bigserial);
insert into bigserial_13 values (-1);
select * from bigserial_13;
drop table bigserial_13;