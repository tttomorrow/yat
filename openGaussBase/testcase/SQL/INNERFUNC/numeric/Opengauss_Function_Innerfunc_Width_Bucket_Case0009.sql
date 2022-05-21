-- @testpoint: width_bucket函数op为非数值类型,部分测试点合理报错
drop table if exists data_01;
create table data_01 (clo1 char,clo2 boolean);
insert into data_01 values ('a',true);
select width_bucket(clo1,2,5,5) from data_01;
select width_bucket(clo2,-3,3,5) from data_01;
select width_bucket(null,2,5,4);
drop table if exists data_01;