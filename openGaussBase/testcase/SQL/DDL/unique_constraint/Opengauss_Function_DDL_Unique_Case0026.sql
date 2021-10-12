-- @testpoint: 使用alter...add语句增加外键约束
-- @modify at: 2020-11-23
--建表1
drop table if exists test_unique_constraint026;
create table test_unique_constraint026(test_unique_constraint026no number(4) primary key,ename varchar2(20),test_unique_constraint026_bakno number(2));
--建表2
drop table if exists test_unique_constraint026_bak;
create table test_unique_constraint026_bak(test_unique_constraint026_bakno number(2) not null unique,dname varchar2(20));
--增加外键约束
alter table test_unique_constraint026 add constraint test_unique_constraint026_test_unique_constraint026_bakno_fk foreign key(test_unique_constraint026_bakno) references test_unique_constraint026_bak(test_unique_constraint026_bakno);
--查询约束信息
select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint026') order by conname;
select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint026_bak') order by conname;
 --删表
 drop table test_unique_constraint026;
 drop table test_unique_constraint026_bak;