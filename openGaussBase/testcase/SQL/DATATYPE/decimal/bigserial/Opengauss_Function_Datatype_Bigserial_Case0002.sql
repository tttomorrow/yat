-- @testpoint: 插入有效负整数

drop table if exists bigserial_02;
create table bigserial_02 (name bigserial);
insert into bigserial_02 values (-1212);
insert into bigserial_02 values (-0004657);
insert into bigserial_02 values (-999999999);
select * from bigserial_02;
drop table bigserial_02;
