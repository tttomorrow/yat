--  @testpoint:建表指定其中一列是唯一约束，冲突后使用insert...nothing语句
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_2a;
--建表指定id列是唯一约束
create table mykey_2a
(
   name nvarchar2(20),
   id number unique ,
   address nvarchar2(50)
) ;

--常规insert语句插入一条数据('bibly',1,'shenzhen')
insert into mykey_2a values('bibly',1,'shenzhen');
select * from mykey_2a;
--唯一列冲突使用insert...nothing语句插入一条数据('lisa1',1,'yunnan'），唯一约束id列重复，直接返回，数据未发生变化
insert into mykey_2a values('lisa1',1,'yunnan') on DUPLICATE KEY UPDATE nothing;
select * from mykey_2a;
--唯一列冲突使用insert...nothing语句插入一条数据('lisa1',2,'yunnan'），唯一约束id列不重复，新增一条数据
insert into mykey_2a values('lisa1',2,'yunnan') on DUPLICATE KEY UPDATE nothing;
select * from mykey_2a;
drop table mykey_2a;