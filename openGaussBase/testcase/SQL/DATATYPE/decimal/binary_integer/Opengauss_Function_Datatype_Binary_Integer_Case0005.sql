-- @testpoint: 插入字符串类型数值

drop table if exists binary_integer05;
create table binary_integer05 (name binary_integer);
insert into binary_integer05 values ('123456');
insert into binary_integer05 values ('-123456');
select * from binary_integer05;
drop table binary_integer05;