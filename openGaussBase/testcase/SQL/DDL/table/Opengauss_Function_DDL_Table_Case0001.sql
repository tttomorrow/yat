-- @testpoint: alter table 修改有空值的列为not null,合理报错
drop table if exists table_alter_001;
create table table_alter_001
(
c1 int,
c2 bigint,
c3 varchar(20)
);
insert into table_alter_001 values('11',null,'sss');
insert into table_alter_001 values('21','','sss');
insert into table_alter_001 values('31',66,'');
insert into table_alter_001 values('41',66,null);

alter table table_alter_001 modify c3 varchar(50);
alter table table_alter_001 modify c3 not null;
insert into table_alter_001 values('','','');
alter table table_alter_001 modify c2 varchar(60);
alter table table_alter_001 modify c1 varchar(60);
drop table if exists table_alter_001;