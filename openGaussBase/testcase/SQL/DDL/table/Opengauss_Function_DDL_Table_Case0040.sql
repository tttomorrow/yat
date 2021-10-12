-- @testpoint: 列存表支持添加字段ADD COLUMN
drop table if exists alter_table_tb040;
create table alter_table_tb040
(
c1 int,
c2 bigint,
c3 varchar(20)
)with(ORIENTATION=COLUMN);
insert into alter_table_tb040 values('11',null,'sss');
insert into alter_table_tb040 values('21','','sss');
insert into alter_table_tb040 values('31',66,'');
insert into alter_table_tb040 values('41',66,null);
insert into alter_table_tb040 values('41',66,null);
ALTER TABLE alter_table_tb040 ADD  COLUMN  c4 char(20);
insert into alter_table_tb040 values('21','','sss','qaz');
select * from alter_table_tb040;
drop table if exists alter_table_tb040;





