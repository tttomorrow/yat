-- @testpoint: 创建复合字段唯一约束
-- @modify at: 2020-11-23
--建表
drop table if exists test_unique_constraint011;
create table test_unique_constraint011 (id_p int not null, lastname varchar(255) not null unique, firstname varchar(255),
address varchar(255), city varchar(255),constraint uc_personid unique (id_p,lastname,firstname,address,city));
--插入数据，成功
insert into test_unique_constraint011 values(1,'mary','','','');
insert into test_unique_constraint011 values(2,'maryss','','','');
insert into test_unique_constraint011 values(1,'jhon','','','');
--查询表信息
select * from test_unique_constraint011;
--通过系统表查询约束信息
 select conname,contype from pg_constraint where conrelid = (select oid from pg_class where relname = 'test_unique_constraint011') order by conname;
--删表
 drop table if exists test_unique_constraint011;