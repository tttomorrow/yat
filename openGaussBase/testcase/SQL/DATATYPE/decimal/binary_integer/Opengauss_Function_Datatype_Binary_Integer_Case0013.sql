-- @testpoint: 插入空值

drop table if exists binary_integer13;
create table binary_integer13 (id int,name binary_integer);
insert into binary_integer13 values (1,'');
insert into binary_integer13 values (2,null);
select * from binary_integer13;
drop table binary_integer13;