--  @testpoint:建表指定其中一列是唯一约束，唯一约束列常规插入重复值，合理报错
drop table if exists mykey_0e;
--建表指定id列是唯一约束
create table mykey_0e
(
   name nvarchar2(20),
   id number unique ,
   address nvarchar2(50)
) ;
--常规insert语句插入两条唯一约束列相同值，合理报错
insert into mykey_0e values('lihua',1,'shenzhen'),('lihua1',1,'shenzhen');
select * from mykey_0e;
drop table mykey_0e;