-- @testpoint: alter table对列存表的非空及空值列进行修改，合理报错


drop table if exists table_alter_032;
create table table_alter_032
(id int not null ,name char(20)not null,class char(10) null,score float(1)
)with(ORIENTATION=COLUMN);
insert into table_alter_032 values(4,'小明',1,87.5);
insert into table_alter_032 values(2,'小红',2,62);
insert into table_alter_032 (id,name,class,score) values(3,'小黄',2,88);
insert into table_alter_032 (id,name,class,score) values(5,'小紫',1,57);
insert into table_alter_032 (id,name,class,score) values(7,'小白',' ',100);
select * from table_alter_032;
alter table  table_alter_032 alter class set not null;
alter table  table_alter_032 alter id  set  null;
alter table  table_alter_032 alter id  drop  not null;
drop table if exists table_alter_032;