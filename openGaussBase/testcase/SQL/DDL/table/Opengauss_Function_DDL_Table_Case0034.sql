-- @testpoint: alter table 删除某列，对应索引及约束均被自动删除，再为该列插入数据时合理报错

drop table if exists table_alter_034;
create table table_alter_034
(id int primary key,name char(20),class char(10),course char(20)default '数学',score float(1)
);
insert into table_alter_034 values(4,'小明',1,'数学',87.5);
insert into table_alter_034 values(2,'小红',2,'数学',62);
insert into table_alter_034 (id,name,class,score) values(3,'小黄',2,88);
insert into table_alter_034 (id,name,class,score) values(5,'小紫',1,57);
insert into table_alter_034 (id,name,class,score) values(7,'小白',1,100);
select * from table_alter_034;
drop index if exists table_alter_034_index;
create index table_alter_034_index on table_alter_034(id);
insert into table_alter_034 values(4,'小明',1,'数学',87.5);
insert into table_alter_034 values(2,'小红',2,'数学',62);
alter table  table_alter_034 DROP column IF EXISTS id  CASCADE ;
insert into table_alter_034 values(4,'小明',1,'数学',87.5);
insert into table_alter_034 values(2,'小红',2,'数学',62);
drop index if exists table_alter_034_index;
drop table if exists table_alter_034;