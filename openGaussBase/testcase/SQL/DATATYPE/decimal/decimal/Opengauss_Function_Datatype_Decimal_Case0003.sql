-- @testpoint: 不指定精度，插入浮点数

drop table if exists decimal_03;
create table decimal_03 (name decimal);
insert into decimal_03 values (12122.12);
insert into decimal_03 values (0.0001);
insert into decimal_03 values (-12122.23);
insert into decimal_03 values (-0.0001);
select * from decimal_03;
drop table decimal_03;
