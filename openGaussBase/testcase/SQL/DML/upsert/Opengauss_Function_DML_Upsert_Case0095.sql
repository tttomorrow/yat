--  @testpoint:建表后再增加唯一约束，使用insert..update语句
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_2e;
--建表不指定唯一约束
create table mykey_2e
(
   name nvarchar2(20) ,
   id number  ,
   address nvarchar2(50)
) ;
--未指定唯一约束使用insert..update语句，正常插入
insert into mykey_2e values('dacong',2,'guangdong') on DUPLICATE KEY UPDATE  address='guangdong';
select * from mykey_2e;
--给id列添加唯一约束
alter table mykey_2e add constraint unique_id unique(id);
--常规插入一条数据
insert into mykey_2e values('wangyun',3,'chongqing');
select * from mykey_2e;
--使用insert..update语句,主键id重复，数据('dacong',2,'guangdong')更改为('lisa1',2,'yunnan')
insert into mykey_2e values('lisa1',2,'yunnan') on DUPLICATE KEY UPDATE  name='lisa1',address='yunnan';
select * from mykey_2e;
drop table mykey_2e;