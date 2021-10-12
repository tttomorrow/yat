--  @testpoint:建表指定其中一列是唯一约束，冲突使用insert...update语句
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_0h;
--建表指定id列是唯一约束
create table mykey_0h
(
   name nvarchar2(20),
   id number unique ,
   address nvarchar2(50)
) ;
--常规insert语句插入一条数据('bibly',1,'shenzhen')
insert into mykey_0h values('bibly',1,'shenzhen');
select * from mykey_0h;
--唯一列冲突使用insert...update语句插入一条数据('lisa1',1,'yunnan'），update 唯一约束id列，合理报错
insert into mykey_0h values('lisa1',1,'yunnan') on DUPLICATE KEY UPDATE id=1;
---唯一列冲突使用insert...update语句插入一条数据('dadong',1,'yunnan'），update name列,原有数据('bibly',1,'shenzhen')更改为('dadong',1,'shenzhen')
insert into mykey_0h values('dadong',1,'yunnan') on DUPLICATE KEY UPDATE name='dadong';
select * from mykey_0h;
--唯一列冲突使用insert...update语句插入一条数据('dadong',1,'yunnan'），update address列,数据('dadong',1,'shenzhen')更改为('dadong',1,'yunnan')
insert into mykey_0h values('dadong',1,'yunnan') on DUPLICATE KEY UPDATE address='yunnan';
select * from mykey_0h;
drop table mykey_0h;

