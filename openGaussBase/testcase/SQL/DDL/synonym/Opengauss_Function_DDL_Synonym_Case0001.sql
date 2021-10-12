-- @testpoint: 创建具有依赖关系的表及其同义词；视图及其同义词；自定义函数及其同义词；存储过程及其同义词
-- @modify at: 2020-11-25
--建表
drop table if exists syn_tab_001;
create table syn_tab_001 (a int,b clob);
--建表的同义词
drop synonym if exists syn_tab_syn_001;
create or replace synonym syn_tab_syn_001 for syn_tab_001;
--建视图
drop view if exists syn_view_001;
create or replace view syn_view_001 as select * from syn_tab_syn_001;
--建视图的同义词
create or replace synonym syn_view_syn_001 for syn_view_001;
--建自定义函数
create or replace function syn_fun_001(c int)return number
as
	d int;
begin
	select count(*) into d from syn_view_syn_001 where a=c;
	return d;
end;
/
--建自定义函数同义词
drop synonym if exists syn_fun_syn_001;
create or replace synonym syn_fun_syn_001 for syn_fun_001;
--建存储过程
create or replace procedure syn_proc_001(a int)
as
c number;
begin
	c:=syn_fun_syn_001(a);
end;
/
--建存储过程同义词
drop synonym if exists syn_proc_syn_001;
create or replace synonym syn_proc_syn_001 for syn_proc_001;
--清理环境：
--删表
drop table syn_tab_001 cascade;
--删除表的同义词
drop synonym if exists syn_tab_syn_001;
--删除视图的同义词
drop synonym syn_view_syn_001;
--删除函数
drop function syn_fun_001;
--删除函数同义词
drop synonym syn_fun_syn_001;
--删除存储过程
drop procedure syn_proc_001;
--删除存储过程同义词
drop synonym if exists syn_proc_syn_001;