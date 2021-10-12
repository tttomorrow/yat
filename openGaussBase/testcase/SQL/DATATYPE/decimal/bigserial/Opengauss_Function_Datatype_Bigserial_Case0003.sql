-- @testpoint: 插入浮点数，四舍五入

drop table if exists bigserial_03;
create table bigserial_03 (name bigserial);
insert into bigserial_03 values (12122.12);
insert into bigserial_03 values (-12122.23);
insert into bigserial_03 values (-0.0000066);
insert into bigserial_03 values (-9999.99999);
select * from bigserial_03;
drop table bigserial_03;
