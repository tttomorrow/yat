-- @testpoint: create 全局临时表

drop table if exists tbl_06;
create global temporary table tbl_06(c_id int,c_d_id int NOT NULL);
insert into tbl_06 values(1,2),(3,4),(45,63);
select * from tbl_06;
drop table if exists tbl_06;
