-- @testpoint: alter table修改表的属主
drop table if exists alter_table_tb010;
create table alter_table_tb010(col1 int, col2 int,col3 int,col4 int);
drop user if exists alt_tb_02 cascade;
create user alt_tb_02 identified by 'gauss_234';
grant ALL PRIVILEGES to alt_tb_02;
ALTER TABLE public.alter_table_tb010 owner to alt_tb_02;
drop user if exists alt_tb_02 cascade;
drop table if exists alter_table_tb010;
