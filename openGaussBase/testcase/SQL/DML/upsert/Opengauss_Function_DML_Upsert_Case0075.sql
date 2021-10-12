--  @testpoint:建表指定两个字段是主键约束,使用insert..nothing语句
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_02;
--建表指定name,id字段为联合主键
create table mykey_02
(
   name nvarchar2(20),
   id number ,
   address nvarchar2(50),
   primary key (name,id)
) ;
--常规插入一条数据
INSERT into mykey_02 values('lily',1,'shanxi');
select * from mykey_02;
--使用insert..nothing语句插入一条数据,主键name值重复，id不重复,新插入一条数据('lily',2,'shandong')
insert into mykey_02 values('lily',2,'shandong') ON  DUPLICATE KEY UPDATE nothing;
select * from mykey_02;
--使用insert..nothing语句插入一条数据,主键name值不重复，id重复,新插入一条数据('jerry',2,'shandong')
insert into mykey_02 values('jerry',2,'shandong') ON  DUPLICATE KEY UPDATE nothing;
select * from mykey_02;
--使用insert..nothing语句插入一条数据,主键name重复，id重复，直接返回，更新0条数据
insert into mykey_02 values('jerry',2,'tianjin') ON  DUPLICATE KEY UPDATE nothing;
select * from mykey_02;
drop table mykey_02;