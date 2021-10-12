-- @testpoint: 插入空值

drop table if exists binary_double15;
create table binary_double15 (id int,name binary_double);
insert into binary_double15 values (1,null);
insert into binary_double15 values (2,'');
select * from binary_double15;
drop table binary_double15;