-- @testpoint: 更新表字段再analyze
drop table if exists tbl_013;
create table tbl_013
(col_tinyint  tinyint,col_smallint  smallint,col_int  integer, col_smallserial  varchar(30),
col_char  char(30),col_boolean   boolean, col_float  float(3) default '3.14159');
insert into tbl_013 values(10,-1562,13,'aa','cc','true',2.36);
insert into tbl_013 values(100,9152,245,'aa','cc','false');
select * from tbl_013;
update tbl_013 set col_char='char十',col_float='5.55',col_boolean='true';
select * from tbl_013;
analyze tbl_013;
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'tbl_013');
drop table if exists tbl_013;