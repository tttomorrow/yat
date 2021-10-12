-- @testpoint: 创建列类型是对象标识符类型的表，给非数值时合理报错
drop table if exists table_2;
create table table_2(a OID);
insert into table_2 values(782);
insert into table_2 values(122);
select * from table_2;
drop table if exists table_2;


drop table if exists table_3;
create table table_3(a OID);
insert into table_3 values(782),(QEW),(9_S);
select * from table_3;
drop table if exists table_3;
