-- @testpoint: 插入字符串类型数值

drop table if exists number_09;
create table number_09 (name number);
insert into number_09 values ('12354563');
insert into number_09 values ('-9999999');
insert into number_09 values ('1235.4563');
insert into number_09 values ('-1235.4563');
select * from number_09;
drop table number_09;