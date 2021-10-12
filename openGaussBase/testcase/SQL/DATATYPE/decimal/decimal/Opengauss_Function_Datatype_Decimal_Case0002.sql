-- @testpoint: 不指定精度，插入有效负整数

drop table if exists decimal_02;
create table decimal_02 (name decimal);
insert into decimal_02 values (-12);
insert into decimal_02 values (-1200345);
select * from decimal_02;
drop table decimal_02;
