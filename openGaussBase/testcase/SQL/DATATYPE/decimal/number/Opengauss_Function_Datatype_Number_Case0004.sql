-- @testpoint: 不指定精度，插入字符串形式浮点数

drop table if exists number_04;
create table number_04 (name number);
insert into number_04 values ('14165132.99999');
insert into number_04 values ('0.99999');
insert into number_04 values ('-14165132.999999');
insert into number_04 values ('-0.999999');
select * from number_04;
drop table number_04;
