-- @testpoint: 插入非法空值，合理报错

drop table if exists bigserial_12;
create table bigserial_12 (id int,name bigserial);
insert into bigserial_12 values (1,' ');
drop table bigserial_12;