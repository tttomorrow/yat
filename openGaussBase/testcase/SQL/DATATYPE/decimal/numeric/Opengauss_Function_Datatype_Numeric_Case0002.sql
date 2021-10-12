-- @testpoint: 不指定精度，插入负整数

drop table if exists numeric_02;
create table numeric_02 (name numeric);
insert into numeric_02 values (-1212);
insert into numeric_02 values (-9999999);
insert into numeric_02 values (-1);
insert into numeric_02 values (-2);
insert into numeric_02 values (-3);
select * from numeric_02;
drop table numeric_02;
