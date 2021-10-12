-- @testpoint: 建临时表char类型，默认值长度设置1024左右
drop table if exists tbl_06;
drop table if exists tbl_06_T02;
drop table if exists tbl_06_T03;
create temporary table tbl_06(
c_varchar char(1025) not null default lpad('asdf',1023,'yes'));
create temporary table tbl_06_T02(
c_varchar char(1025) not null default lpad('asdf',1024,'yes'));
create temporary table tbl_06_T03(
c_varchar char(1025) not null default lpad('asdf',1025,'yes'));
drop table tbl_06;
drop table tbl_06_T02;
drop table tbl_06_T03;