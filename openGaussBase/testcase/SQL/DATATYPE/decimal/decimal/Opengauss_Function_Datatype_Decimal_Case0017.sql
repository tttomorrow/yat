-- @testpoint: 指定精度&标度超出合理范围值，合理报错
-- @modified at: 2020-11-23

--指定精度超出左边界范围1
drop table if exists decimal_17;
create table decimal_17 (name decimal(0,2));

--指定精度超出右边界范围1000
drop table if exists decimal_17;
create table decimal_17 (name decimal(1001,2));

--指定标度超出左边界范围值
drop table if exists decimal_17;
create table decimal_17 (name decimal(5,-1));

--指定标度超出精度范围值
drop table if exists decimal_17;
create table decimal_17 (name decimal(10,12));