-- @testpoint: with语句查询中，使用同义词
-- @modify at: 2020-11-25
--建表
drop table if exists syn_table_0037 cascade;
create table syn_table_0037(id int, pid int,name varchar(10));
--插入数据
insert into syn_table_0037 values(2 , 0 , 'a');
insert into syn_table_0037 values(1 , 0 , 'b');
insert into syn_table_0037 values(3 , 2 , 'c');
insert into syn_table_0037 values(4 , 2 , 'd') ;
insert into syn_table_0037 values(5 , 2 , 'e');
insert into syn_table_0037 values(6 , 2 , 'f') ;
insert into syn_table_0037 values(7 , 3 , 'g');
insert into syn_table_0037 values(8 , 3 , 'h') ;
insert into syn_table_0037 values(9 , 4 , 'i');
insert into syn_table_0037 values(10 , 5 , 'j') ;
insert into syn_table_0037 values(11 , 7 , 'k');
insert into syn_table_0037 values(12 , 2 , 'l') ;
insert into syn_table_0037 values(13 , 9 , 'm');
insert into syn_table_0037 values(14 , 9 , 'n') ;
insert into syn_table_0037 values(15 , 4 , 'o');
--创建表的同义词
drop synonym if exists syn_table_0037_bak;
create synonym syn_table_0037_bak  for syn_table_0037;
--with recursive语句使用临时表
with recursive temp_syn_table_0037(t_pid,t_name) as(select distinct pid,name from syn_table_0037_bak)select * from temp_syn_table_0037;
--清理数据
drop table if exists syn_table_0037 cascade;
drop synonym if exists syn_table_0037_bak;