-- @testpoint: 插入字符串类型，合理报错

drop table if exists float09;
create table float09 (name float);
insert into float09 values ('123abc');
insert into float09 values ('1235ss4563');
insert into float09 values ('abc456');
drop table float09;