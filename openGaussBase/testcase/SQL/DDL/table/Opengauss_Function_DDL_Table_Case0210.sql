-- @testpoint: alter table对多个列设置联合主键，合理报错
drop table if exists alter_table_tb008;
create table alter_table_tb008(col1 int, col2 int,col3 int,col4 int);
create unique index test_hsf on alter_table_tb008(col1,col2);
ALTER TABLE alter_table_tb008 ADD CONSTRAINT CON_HSF PRIMARY KEY(col1,col2);
ALTER TABLE alter_table_tb008 ADD CONSTRAINT CON_HSF2 PRIMARY KEY(col1,col2,col3); --error
ALTER TABLE alter_table_tb008  DROP CONSTRAINT  CON_HSF;
ALTER TABLE alter_table_tb008  DROP CONSTRAINT  CON_HSF2; --error
ALTER TABLE alter_table_tb008 ADD CONSTRAINT CON_HSF3 PRIMARY KEY(col1,col2);
ALTER TABLE alter_table_tb008 ADD CONSTRAINT CON_HSF4 PRIMARY KEY(col1,col2,col3); --error
select * from ALTER_TABLE_TB008 order by 1,2;
drop table if exists alter_table_tb008;