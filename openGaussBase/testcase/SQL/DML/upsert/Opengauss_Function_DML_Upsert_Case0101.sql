--  @testpoint:建表时分别指定唯一约束，主键约束，主键和唯一约束都冲突的情况下，使用insert..update..excluded语句
--预置条件enable_upsert_to_merge为off
drop table if exists mykey_4b;
--建表指定id为主键约束，name为唯一约束
create table mykey_4b
(
   name nvarchar2(20) unique ,
   id number primary key ,
   address nvarchar2(50)
) ;

--使用insert语句常规插入两条数据，主键列，唯一列均不重复，插入两条数据
insert into mykey_4b values('tiya',99,'daqing'),('tiya1',100,'beijing');
select * from mykey_4b;
--使用insert..update..excluded语句，主键和唯一约束都重复，更改后的数据是('tiya',99,'yunnan'),('tiya1',100,'dali')
 insert into mykey_4b values('tiya',99,'yunnan'),('tiya1',100,'dali')on DUPLICATE KEY UPDATE address=excluded.address;
 select * from mykey_4b;
 drop table mykey_4b;