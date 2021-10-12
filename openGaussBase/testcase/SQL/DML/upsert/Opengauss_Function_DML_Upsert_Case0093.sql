--  @testpoint:建表指定两列是唯一约束，使用insert ...update..EXCLUDED语句,多行冲突，只更新第一行数据
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_2c;
--建表指定name和id列是唯一约束
create table mykey_2c
(
   name nvarchar2(20) unique,
   id number unique ,
   address nvarchar2(50)
) ;
--常规插入唯一约束列两条不重复的数据
insert into mykey_2c values ('dacong',2,'shandong'),('liuhua',3,'qingdao');
select * from mykey_2c;
--使用insert ...update..EXCLUDED语句，id和name唯一约束列有两行冲突，数据更改为('dacong',2,'guangdong')且新增一条数据('liuhua',3,'jilin')
insert into mykey_2c values('dacong',2,'guangdong'),('liuhua',3,'jilin') on DUPLICATE KEY UPDATE  address=EXCLUDED.address;
select * from mykey_2c;
drop table mykey_2c;

