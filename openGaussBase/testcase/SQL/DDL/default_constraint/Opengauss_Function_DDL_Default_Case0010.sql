-- @testpoint: 建表default关键字写错,合理报错

drop table if exists tbl_01;
create table tbl_01(
drop table tbl_01;