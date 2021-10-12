-- @testpoint: drop table RESTRICT删除，有依赖对象时合理报错
drop table if exists alter_table_tb02;
create table alter_table_tb02
(
c1 int,
c2 bigint,
c3 varchar(20)
);
insert into alter_table_tb02 values('11',null,'sss');
insert into alter_table_tb02 values('21','','sss');
insert into alter_table_tb02 values('31',66,'');
insert into alter_table_tb02 values('41',66,null);
insert into alter_table_tb02 values('41',66,null);
CREATE VIEW myView AS
    SELECT * FROM alter_table_tb02 ;
SELECT * FROM myView ;

drop table if exists alter_table_tb02 RESTRICT;
drop table if exists alter_table_tb02 CASCADE;



