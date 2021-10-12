--  @testpoint:建表后再增加唯一约束，使用insert..update..EXCLUDED语句
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_2g;
--建表不指定唯一约束
create table mykey_2g
(
   name nvarchar2(20) ,
   id number  ,
   address nvarchar2(50)
) ;
--未指定唯一约束使用insert..update..EXCLUDED语句，正常插入
insert into mykey_2g values('dacong',2,'guangdong') on DUPLICATE KEY UPDATE  address=EXCLUDED.address;
select * from mykey_2g;
--给id列添加唯一约束
alter table mykey_2g add constraint unique_id unique(id);
--常规插入一条数据
insert into mykey_2g values('wangyun',3,'chongqing');
select * from mykey_2g;
--使用insert..update..EXCLUDED语句,主键id重复，数据('wangyun',2,'chongqing')更改为('lisa1',2,'yunnan')
insert into mykey_2g values('lisa1',2,'yunnan') on DUPLICATE KEY UPDATE  name=EXCLUDED.name,address=EXCLUDED.address;
select * from mykey_2g;
drop table mykey_2g;