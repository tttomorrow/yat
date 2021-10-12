-- @testpoint: alter列存表的default值
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
alter table  table_alter_031 alter course set default '';
insert into table_alter_031 (id,name,class,score) values(3,'小黄',2,88);
insert into table_alter_031 (id,name,class,score) values(5,'小紫',1,57);
select * from table_alter_031;
alter table  table_alter_031 alter course set default 'math';
insert into table_alter_031 (id,name,class,score) values(3,'小黄',2,88);
insert into table_alter_031 (id,name,class,score) values(5,'小紫',1,57);
insert into table_alter_031 (id,name,class,score) values(7,'小白',1,100);
select * from table_alter_031;
alter table  table_alter_031 alter course drop default;
insert into table_alter_031 values(4,'小明',1,'数学',87.5);
insert into table_alter_031 values(2,'小红',2,'数学',62);
insert into table_alter_031 (id,name,class,score) values(3,'小黄',2,88);
insert into table_alter_031 (id,name,class,score) values(5,'小紫',1,57);
select * from table_alter_031;
drop table if exists table_alter_031;