-- @testpoint: 列存表支持修改字段的数据类型
drop table if exists alter_table_tb041;
create table alter_table_tb041
(
c1 int,
c2 bigint,
c3 varchar(20)
)with(ORIENTATION=COLUMN);
insert into alter_table_tb041 values('11',null,'sss');
insert into alter_table_tb041 values('21','','sss');
insert into alter_table_tb041 values('31',66,'');
insert into alter_table_tb041 values('41',66,null);
insert into alter_table_tb041 values('41',66,null);
ALTER TABLE alter_table_tb041  MODIFY (c3  char(20)) ;
drop table if exists alter_table_tb041;