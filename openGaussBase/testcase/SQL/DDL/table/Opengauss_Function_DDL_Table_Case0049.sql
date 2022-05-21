-- @testpoint: create 相同的表名的表，合理报错
drop table if exists tb_1;
create table tb_1(id int);
create table tb_1(id char);
drop table if exists tb_1;
 
