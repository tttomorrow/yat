--  @testpoint:创建表时指定唯一约束，使用insert..update语句后再删除唯一约束
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_3d;
--建表指定id唯一约束
create table mykey_3d
(
   name nvarchar2(20) ,
   id number unique ,
   address nvarchar2(50)
) ;
--使用insert..update语句插入两行数据，主键重复，数据更改为('lisa1',2,'yunnan')
insert into mykey_3d values('lisa10',2,'yunnan'),('tom',2,'tianjin') on DUPLICATE KEY UPDATE name='lisa1',address='yunnan';
--使用insert..update语句插入两行数据，主键不重复，插入两条数据
insert into mykey_3d values('lisa10',3,'yunnan'),('tom',4,'tianjin') on DUPLICATE KEY UPDATE name='lisa1',address='yunnan';
select * from mykey_3d;
--删除唯一约束
alter table mykey_3d drop CONSTRAINT mykey_3d_id_key;
--使用insert..update语句插入两行数据，新增两条数据('lisa10',2,'yunnan'),('tom',2,'tianjin')
insert into mykey_3d values('lisa10',2,'yunnan'),('tom',2,'tianjin') on DUPLICATE KEY UPDATE name='lisa1',address='yunnan';
select * from mykey_3d;
drop table mykey_3d;