-- @testpoint: 不指定精度，插入正整数

drop table if exists numeric_01;
create table numeric_01 (name numeric);
insert into numeric_01 values (120);
insert into numeric_01 values (9999999);
insert into numeric_01 values (1);
insert into numeric_01 values (2);
insert into numeric_01 values (3);
select * from numeric_01;
drop table numeric_01;