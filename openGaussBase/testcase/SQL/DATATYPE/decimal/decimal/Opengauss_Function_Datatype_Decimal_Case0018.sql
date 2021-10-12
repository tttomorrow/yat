-- @testpoint: 指定精度&标度合理范围值，插入数据超出标度范围值，四舍五入自动截取

drop table if exists decimal_18;
create table decimal_18 (name decimal(6,2));
insert into decimal_18 values (0.123);
insert into decimal_18 values (123.12656);
select * from decimal_18;
drop table decimal_18;