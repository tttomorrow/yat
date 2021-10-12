--  @testpoint:建表指定主键约束，使用insert..update同一语句，插入两条数据，主键重复
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_3f;
--建表指定id为主键约束
create table mykey_3f
(
   name nvarchar2(20) ,
   id number primary key ,
   address nvarchar2(50)
) ;
--使用insert..update语句插入两行数据，主键重复，数据更新为('lisa1',2,'yunnan')
insert into mykey_3f values('lisa10',2,'yunnan'),('tom',2,'tianjin') on DUPLICATE KEY UPDATE name='lisa1',address='yunnan';
select * from mykey_3f;
drop table  mykey_3f;
