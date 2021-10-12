-- @testpoint: default含特殊英文字，合理报错
drop table if exists tbl_08;
-- @testpoint: 特殊字符
create table tbl_08(id int,c_name varchar(1023) not null default 'afff1212!@#-|;<>?/.,');
-- @testpoint: 含单引号报错
create table tbl_08_02(id int,c_varchar varchar(1023) not null default ''aaaaffff1212'');
insert into tbl_08 values(1,default);
insert into tbl_08(id) values(2);
select * from tbl_08;
drop table tbl_08;