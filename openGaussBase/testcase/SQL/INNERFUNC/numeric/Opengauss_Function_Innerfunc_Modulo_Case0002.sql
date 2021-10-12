-- @testpoint: 数字操作符%(求余),浮点型数据相余
drop table if exists data_01;
create table data_01 (clo1 FLOAT(3),clo2 FLOAT4);
insert into data_01 values (255.00001, 32767.1234587);
select * from data_01;
select clo1 % clo2 from data_01;
drop table if exists data_01;