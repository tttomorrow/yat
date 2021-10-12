-- @testpoint: 列存表支持更改表名称
drop table if exists table_alter_043;
create table table_alter_043
(id int,name char(20),class char(10),course char(20)default '数学',score float(1)
)with(ORIENTATION=COLUMN);
insert into table_alter_043 values(4,'小明',1,'数学',87.5);
insert into table_alter_043 values(2,'小红',2,'数学',62);
insert into table_alter_043 (id,name,class,score) values(3,'小黄',2,88);
insert into table_alter_043 (id,name,class,score) values(5,'小紫',1,57);
insert into table_alter_043 (id,name,class,score) values(7,'小白',1,100);
ALTER TABLE  IF EXISTS  table_alter_043 RENAME TO alter_table_043;
drop table if exists alter_table_043;