--  @testpoint:建表指定其中一列是唯一约束，唯一约束列常规插入不重复值
drop table if exists mykey_0d;
--建表指定id列是唯一约束
create table mykey_0d
(
   name nvarchar2(20),
   id number unique ,
   address nvarchar2(50)
) ;
--常规insert语句插入两条唯一约束列不同值，插入成功
insert into mykey_0d values('lihua',1,'shenzhen'),('lihua1',2,'shenzhen');
select * from mykey_0d;
drop table mykey_0d;