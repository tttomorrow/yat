--  @testpoint:建表指定两个字段是主键约束,使用insert..into语句并加关键字EXCLUDED
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_01;
--建表指定name,id字段为联合主键
create table mykey_01
(
   name nvarchar2(20),
   id number ,
   address nvarchar2(50),
   primary key (name,id)
) ;
--常规插入一条数据
INSERT into mykey_01 values('lily',1,'shanxi');
select * from mykey_01;
--使用insert..into语句插入一条数据，主键name值重复，id不重复,新增一条数据('lily',2,'shandong')
insert into mykey_01 values('lily',2,'shandong') ON  DUPLICATE KEY UPDATE address=EXCLUDED.address;
select * from mykey_01;
--使用insert..into语句插入一条数据，主键name值不重复，id重复,新增一条数据('lisa',2,'shandong')
insert into mykey_01 values('lisa',2,'shandong') ON DUPLICATE KEY UPDATE address=EXCLUDED.address;
select * from mykey_01;
--使用insert..into语句插入一条数据，主键name和id都重复，原有数据('lisa',2,'shandong')修改为('lisa',2,'dalian')
insert into mykey_01 values('lisa',2,'dalian') ON DUPLICATE KEY UPDATE address=EXCLUDED.address;
select * from mykey_01;
drop table mykey_01;