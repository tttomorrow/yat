-- @testpoint: 自定义函数同义词与case when结合使用
-- @modify at: 2020-11-25
--建表
drop table if exists syn_tab_001 cascade;
create table syn_tab_001 (a int,b clob);
--建视图
drop view if exists syn_view_001 cascade ;
create or replace view syn_view_001 as select * from syn_tab_001;
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
--创建函数
drop function if exists syn_fun_005;
create or replace function syn_fun_005(c int)  return int
as
c int;
d int :=0;
begin
	case
	when syn_fun_syn_001(c)<0 then
		d := 1;
	when syn_fun_syn_001(c)=0 then
		d := 2;
	else
		d := 3;
	end case;
	return d;
end;
/

--调用函数
select syn_fun_001(-1);
select syn_fun_001(0);
select syn_fun_001(1);
--清理环境
drop function if exists  syn_fun_001;
drop function if exists syn_fun_005;
drop table if exists syn_tab_001 cascade;
drop synonym if exists syn_view_syn_001;