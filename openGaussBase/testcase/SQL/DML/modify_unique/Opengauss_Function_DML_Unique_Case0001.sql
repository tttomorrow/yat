-- @testpoint: 创建列为tab1_unique的测试表，并修改其约束为unique，再次更新唯一约束列,约束名已存在，合理报错

drop table if exists tab1;
create table tab1(tab1_unique  int);
alter table tab1 add constraint un unique (tab1_unique);
alter table tab1 add  column  tab1_id  char(30);
select * from  tab1;
alter table tab1 add constraint un unique(tab1_id );
drop table tab1;
