-- @testpoint: default含特殊英文字符1

drop table if exists tbl_09;
create table tbl_09(
id int,
c_varchar varchar(1023) not null default 'aaaaaaadddsfdsfdsfdfsfdsffffffffffff1212!@#$%^&*(_+=-');
insert into tbl_09 values(1,default);
insert into tbl_09(id) values(2);
 select * from tbl_09;
drop table tbl_09;