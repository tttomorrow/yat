-- @testpoint: 数字操作符|/(平方根),0值进行开平方
drop table if exists data_01;
create table data_01 (clo1 int,clo2 BIGINT);
insert into data_01 values (0, 0);
select |/clo1,|/clo2 from data_01;
drop table if exists data_01;