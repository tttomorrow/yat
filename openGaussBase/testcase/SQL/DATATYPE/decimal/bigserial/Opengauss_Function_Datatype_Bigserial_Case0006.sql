-- @testpoint: 插入超出左边界范围值，隐式转换bigint

drop table if exists bigserial_06;
create table bigserial_06 (name bigserial);
insert into bigserial_06 values (0);
select * from bigserial_06;
drop table bigserial_06;