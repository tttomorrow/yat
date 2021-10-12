-- @testpoint: analyze字段含有约束的表

drop table if exists tbl_009;
create table tbl_009
(col_tinyint  tinyint,col_smallint  smallint,col_int  integer, col_smallserial varchar(30),
col_char  char(30),col_boolean boolean, col_float float(3) default '3.14159');
insert into tbl_009 values(10,-1562,13,'aa','cc','true',2.36);
insert into tbl_009 values(100,9152,245,'aa','cc','false');
analyze tbl_009;
drop table if exists tbl_009;