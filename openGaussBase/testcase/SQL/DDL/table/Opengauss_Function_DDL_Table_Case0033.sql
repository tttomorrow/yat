-- @testpoint: 重建表索引
drop table if exists table_alter_031;
create table table_alter_031
(id int,name char(20),class char(10),course char(20)default '数学',score float(1)
)with(ORIENTATION=COLUMN);
insert into table_alter_031 values(4,'小明',1,'数学',87.5);
insert into table_alter_031 values(2,'小红',2,'数学',62);
insert into table_alter_031 (id,name,class,score) values(3,'小黄',2,88);
insert into table_alter_031 (id,name,class,score) values(5,'小紫',1,57);
insert into table_alter_031 (id,name,class,score) values(7,'小白',1,100);
select * from table_alter_031;
DROP INDEX if exists table_alter_031_index;
create index table_alter_031_index on table_alter_031(id);
ALTER INDEX table_alter_031_index REBUILD;
create index table_031_index on table_alter_031(id);
DROP INDEX if exists table_alter_031_index;
drop table if exists table_alter_031;