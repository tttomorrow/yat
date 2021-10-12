-- @testpoint: ceiling函数入参为正负无穷大
drop table if exists data_01;
create table data_01 (clo1 float,clo2 float);
insert into data_01 values ('Infinity','-Infinity');
select ceiling(clo1), ceiling(clo2) from data_01;
drop table if exists data_01;