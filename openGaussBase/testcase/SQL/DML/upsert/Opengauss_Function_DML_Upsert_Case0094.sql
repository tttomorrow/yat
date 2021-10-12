--  @testpoint:建表指定两列是唯一约束，使用insert ...nothing语句
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_2d;
--建表指定name和id列是唯一约束
create table mykey_2d
(
   name nvarchar2(20) unique,
   id number unique ,
   address nvarchar2(50)
) ;
--常规插入唯一约束列两条不重复的数据
insert into mykey_2d values ('dacong',2,'shandong'),('liuhua',3,'qingdao');
select * from mykey_2d;
--使用insert ...nothing语句，插入两条数据唯一约束列数据重复，直接返回，数据未发生变化
insert into mykey_2d values('dacong',2,'guangdong'),('liuhua',3,'jilin') on DUPLICATE KEY UPDATE nothing;
select * from mykey_2d;
--用insert ...nothing语句，插入两条数据，唯一约束列数据不重复，新增两条数据
insert into mykey_2d values('lisi',6,'xian'),('xiaozi',8,'jilin') on DUPLICATE KEY UPDATE nothing;
select * from mykey_2d;
--用insert ...nothing语句，插入两条数据，第一条数据唯一约束列重复，第二条唯一约束列数据不重复，新增一条数据('omm',9,'jilin')
insert into mykey_2d values('lisi',6,'xianyang'),('omm',9,'jilin') on DUPLICATE KEY UPDATE nothing;
select * from mykey_2d;
drop table mykey_2d;