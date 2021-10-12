-- @testpoint: 插入字符串类型,合理报错

drop table if exists smallserial_09;
create table smallserial_09 (name smallserial);
insert into smallserial_09 values ('123abc');
insert into smallserial_09 values ('1235ss4563');
insert into smallserial_09 values ('abc456');
drop table smallserial_09;