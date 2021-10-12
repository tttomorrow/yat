-- @testpoint: 插入bool类型

drop table if exists binary_integer06;
create table binary_integer06 (name binary_integer);
insert into binary_integer06 values ('1');
insert into binary_integer06 values ('0');
insert into binary_integer06 values (true);
insert into binary_integer06 values (false);
select * from binary_integer06;
drop table binary_integer06;