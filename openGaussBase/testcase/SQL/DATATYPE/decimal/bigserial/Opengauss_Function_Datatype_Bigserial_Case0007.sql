-- @testpoint: 插入超出右边界范围值，合理报错

drop table if exists bigserial_07;
create table bigserial_07 (name bigserial);
insert into bigserial_07 values (9223372036854775808);
select * from bigserial_07;
drop table  bigserial_07;
