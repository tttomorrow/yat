-- @testpoint: 插入0值

drop table if exists binary_double14;
create table binary_double14 (name binary_double);
insert into binary_double14 values (0);
select * from binary_double14;
drop table binary_double14;