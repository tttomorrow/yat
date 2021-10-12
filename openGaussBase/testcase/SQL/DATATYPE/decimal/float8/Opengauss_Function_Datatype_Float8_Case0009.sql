-- @testpoint: 插入字符串类型，合理报错

drop table if exists float8_09;
create table float8_09 (name float8);
insert into float8_09 values ('123abc');
insert into float8_09 values ('1235ss4563');
insert into float8_09 values ('abc456');
drop table float8_09;