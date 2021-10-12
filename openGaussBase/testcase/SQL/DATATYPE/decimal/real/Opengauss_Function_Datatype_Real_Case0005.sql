-- @testpoint: 插入字符串类型,合理报错

drop table if exists real_05;
create table real_05 (name real);
insert into real_05 values ('123abc');
insert into real_05 values ('1235ss4563');
insert into real_05 values ('abc456');
drop table real_05;