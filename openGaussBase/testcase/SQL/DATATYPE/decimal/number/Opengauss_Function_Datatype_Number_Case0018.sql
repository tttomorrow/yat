-- @testpoint: 指定精度&标度合理范围值，插入数据超出标度范围值，四舍五入自动截取

drop table if exists number_18;
create table number_18 (name number(6,2));
insert into number_18 values (0.123);
insert into number_18 values (123.12656);
select * from number_18;
drop table number_18;