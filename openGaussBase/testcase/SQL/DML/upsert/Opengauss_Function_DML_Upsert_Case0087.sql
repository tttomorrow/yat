--  @testpoint:建表指定其中一列是唯一约束，唯一约束列常规插入null值,插入成功
drop table if exists mykey_0f;
--建表指定id列是唯一约束
create table mykey_0f
(
   name nvarchar2(20),
   id number unique ,
   address nvarchar2(50)
) ;
--常规insert语句插入一条数据，唯一约束列为null值
insert into mykey_0f values('bibly',null,'shenzhen');
select * from mykey_0f;
--常规insert语句插入一条数据，唯一约束列为null值
insert into mykey_0f(name,address) values('lihua1','shenzhen');
select * from mykey_0f;
drop table mykey_0f;