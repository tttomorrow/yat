-- @testpoint: 不指定精度，插入有效正整数

drop table if exists decimal_01;
create table decimal_01 (name decimal);
insert into decimal_01 values (12);
insert into decimal_01 values (1200034);
insert into decimal_01 values (9999999999);
select * from decimal_01;
drop table decimal_01;