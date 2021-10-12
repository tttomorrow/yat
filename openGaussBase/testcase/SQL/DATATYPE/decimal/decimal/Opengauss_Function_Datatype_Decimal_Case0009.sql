-- @testpoint: 插入字符串类型,合理报错

drop table if exists decimal_09;
create table decimal_09 (name decimal);
insert into decimal_09 values ('abc');
insert into decimal_09 values ('1235ss4563');
insert into decimal_09 values ('abc456');
drop table decimal_09;