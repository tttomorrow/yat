--  @testpoint:建表指定其中一列是唯一约束并加非空约束，唯一约束列常规插入null值,合理报错
drop table if exists mykey_0g;
--建表指定id列是唯一约束
create table mykey_0g
(
   name nvarchar2(20),
   id number unique not null ,
   address nvarchar2(50)
) ;
--常规insert语句插入一条数据，唯一约束列为null值
insert into mykey_0g values('bibly',null,'shenzhen');
select * from mykey_0g;
--常规insert语句插入一条数据，唯一约束列为null值
insert into mykey_0g(name,address) values('lihua1','shenzhen');
select * from mykey_0g;
drop table mykey_0g;