-- @testpoint: 插入空值,合理报错

drop table if exists bigserial_14;
create table bigserial_14 (id int,name bigserial);
insert into bigserial_14 values (1,null);
insert into bigserial_14 values (2,'');
drop table bigserial_14;