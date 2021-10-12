-- @testpoint: --创建主键约束区别大小写 合理报错
drop table if exists false_2;
create table false_2(a int,b int);

drop table if exists false_3;
create table false_3(a int,b int);
--字段大小写不同
alter table false_2 add constraint qq primary key(B);
alter table false_2 add constraint qq primary key(b);
--约束名称大小写不同
alter table false_3 add constraint PP primary key(a);
alter table false_3 add constraint pp primary key(a);

SELECT conname,contype,condeferrable,condeferred,convalidated FROM PG_CONSTRAINT WHERE conname in ('qq','pp');

alter table false_2 drop constraint qq;
alter table false_2 drop constraint QQ;
alter table false_3 drop constraint pp;
alter table false_3 drop constraint PP;
SELECT conname,contype,condeferrable,condeferred,convalidated FROM PG_CONSTRAINT WHERE conname in ('qq','pp');

drop table if exists false_2;
drop table if exists false_3;

