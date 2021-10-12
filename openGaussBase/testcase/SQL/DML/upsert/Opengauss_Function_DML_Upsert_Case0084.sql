--  @testpoint:建表时指定id列是主键，后修改name列是主键，使用insert..nothing插入数据
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_0c;
--建表指定id字段为主键
create table mykey_0c
(
   name nvarchar2(20),
   id number primary key ,
   address nvarchar2(50)
) ;
--常规insert插入一条数据
insert into mykey_0c values('kihy',5,'jinhua');
select * from mykey_0c;
--使用insert..nothing语句,主键冲突，直接返回，数据未发生变化
insert into mykey_0c values('lisa',5,'dalian') ON DUPLICATE KEY UPDATE nothing;
select * from mykey_0c;
--删除id列的主键约束
alter table mykey_0c drop constraint mykey_0c_pkey;
--常规插入id已存在的值，合理插入
insert into mykey_0c values('liqi',5,'dalian');
select * from mykey_0c;
--使用insert..nothing，id存在，新增一条数据('lisa1',5,'yunnan'),正常插入
INSERT INTO mykey_0c VALUES('lisa1',5,'yunnan') ON DUPLICATE KEY UPDATE nothing;
select * from mykey_0c;
drop table mykey_0c;