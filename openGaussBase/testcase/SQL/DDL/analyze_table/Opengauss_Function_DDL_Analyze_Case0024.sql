-- @testpoint: analyze单列表
drop table if exists tbl_011;
drop table if exists tbl_012;
create table tbl_011 (col_tinyint  tinyint );
create table tbl_012 ( col_tinyint   tinyint);
insert into tbl_011 values(183);
insert into tbl_012 (select col_tinyint from tbl_011);
analyze  tbl_012 ;
drop table if exists tbl_011;
drop table if exists tbl_012;