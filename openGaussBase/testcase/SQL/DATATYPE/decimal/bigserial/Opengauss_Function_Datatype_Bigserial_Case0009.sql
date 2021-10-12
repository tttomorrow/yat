-- @testpoint: 插入字符串类型，合理报错

drop table if exists bigserial_09;
create table bigserial_09 (name bigserial);
insert into bigserial_09 values ('123abc');
insert into bigserial_09 values ('1235ss4563');
insert into bigserial_09 values ('abc456');
drop table bigserial_09;