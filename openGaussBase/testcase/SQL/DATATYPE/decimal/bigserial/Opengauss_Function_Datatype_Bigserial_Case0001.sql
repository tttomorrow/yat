-- @testpoint: 插入有效正整数

drop table if exists bigserial_01;
create table bigserial_01 (name bigserial);
insert into bigserial_01 values (120);
insert into bigserial_01 values (0004567);
select * from bigserial_01;
drop table bigserial_01;