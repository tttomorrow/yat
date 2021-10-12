-- @testpoint: 自定义函数作为入参与函数自己嵌套10层使用
-- @modify at: 2020-11-25
drop function if exists syn_fun_007;
--创建自定义函数
create or replace function syn_fun_007(c bigint) return int
as
  b int := c;
begin
	for i in 1..c loop
		b := b + 1;
	end loop;
	return b;
end;
/
--建自定义函数同义词
drop synonym if exists syn_fun_syn_007;
create or replace synonym syn_fun_syn_007 for syn_fun_007;
--嵌套调用
select syn_fun_syn_007(syn_fun_syn_007(syn_fun_syn_007(syn_fun_syn_007(syn_fun_syn_007(syn_fun_syn_007(syn_fun_syn_007(syn_fun_syn_007(syn_fun_syn_007(syn_fun_syn_007(1)))))))))) from sys_dummy;
--删除函数
drop function if exists syn_fun_007;
--删除同义词
drop synonym syn_fun_syn_007;