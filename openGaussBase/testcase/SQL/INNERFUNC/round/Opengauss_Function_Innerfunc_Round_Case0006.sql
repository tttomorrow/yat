-- @testpoint: round函数入参超出范围，合理报错
drop table if exists tb;
create table tb (dp1 double precision);
insert into tb values (9.8);
insert into tb values (round(cast(12.3 as double precision) ,cast(123.5 as double precision),cast(123.65 as double precision)));
update tb set dp1=round(cast(12.3 as numeric),cast(123.5 as nemeric),cast(123.65 as numeric)) where dp1=9.8;
select round(cast(12.3 as double precision) ,cast(123.5 as nemeric),cast(123.65 as numeric)) as result;
drop table tb;