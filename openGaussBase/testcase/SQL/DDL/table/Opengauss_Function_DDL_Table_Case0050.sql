-- @testpoint: create 本地临时表

drop table if exists tbl_05;
create local temporary table tbl_05(c_id int,c_d_id int NOT NULL);
insert into tbl_05 values(1,2),(3,4),(45,63);
select * from tbl_05;
drop table if exists tbl_05;
 
