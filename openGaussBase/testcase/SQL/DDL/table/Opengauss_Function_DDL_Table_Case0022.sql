-- @testpoint: alter table修改默认空的列为非空，在已有空值时合理报错
--参数

--default ''
drop table if exists alter_table_tb001;
create table alter_table_tb001
(
c1 varchar(20)  default '' ,
c2 varchar(20)  default '' ,
c3 varchar(20)  default '' 
);
insert into alter_table_tb001 values('11',null,'sss');
insert into alter_table_tb001 values('21','','sss');
insert into alter_table_tb001 values('31',66,'');
insert into alter_table_tb001 values('41',66,null);

alter table alter_table_tb001 modify c3 varchar(50);
alter table alter_table_tb001 modify c3  not null;
insert into alter_table_tb001 values('','','');
alter table alter_table_tb001 modify c2 varchar(60);
alter table alter_table_tb001 modify c1 varchar(60);
--default null
drop table if exists alter_table_tb001;
create table alter_table_tb001
(
c1 int  default null ,
c2 bigint  default null,
c3 varchar(20)  default null 
);
insert into alter_table_tb001 values('11',null,'sss');
insert into alter_table_tb001 values('21','','sss');
insert into alter_table_tb001 values('31',66,'');
insert into alter_table_tb001 values('41',66,null);

alter table alter_table_tb001 modify c3 varchar(50);
alter table alter_table_tb001 modify c3  not null;
insert into alter_table_tb001 values('','','');
alter table alter_table_tb001 modify c2 varchar(60);
alter table alter_table_tb001 modify c1 varchar(60);
drop table if exists alter_table_tb001;