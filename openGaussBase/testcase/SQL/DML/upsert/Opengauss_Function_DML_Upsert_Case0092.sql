--  @testpoint:建表指定两列是唯一约束，使用insert ...update语句,多行冲突，只更新第一行数据
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_2b;
--建表指定name和id列是唯一约束
create table mykey_2b
(
   name nvarchar2(20) unique,
   id number unique ,
   address nvarchar2(50)
) ;
--常规插入唯一约束列两条不重复的数据
insert into mykey_2b values ('dacong',2,'shandong'),('liuhua',3,'qingdao');
select * from mykey_2b;
--使用insert ...update语句，id和name唯一约束列有两行冲突，更改后的数据('dacong',2,'guangdong')和('liuhua',3,'guangdong')
insert into mykey_2b values('dacong',2,'guangdong'),('liuhua',3,'jilin') on DUPLICATE KEY UPDATE  address='guangdong';
select * from mykey_2b;
drop table mykey_2b;


