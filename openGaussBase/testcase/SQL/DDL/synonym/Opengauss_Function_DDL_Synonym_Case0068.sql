-- @testpoint: 创建函数的同义词，修改同义词属主（属主为存在+不存在+存在无create权限）,不存在+存在无create权限,合理报错
--建自定义函数
drop function if exists SYN_FUN_068_001(c int);
create or replace function SYN_FUN_068_001(c int)return number
as
b int := c;
begin
	for i in 1..c loop
		b:= b - 1;
	end loop;
	return b;
end;
/
--建自定义函数同义词
drop synonym if exists SYN_FUN_SYN_068_001 cascade ;
create or replace synonym SYN_FUN_SYN_068_001 for SYN_FUN_068_001;
--创建用户
drop user if exists syn005;
create user syn005 password 'Test@123';
--修改为存在的属主：新属主无create权限：报错
alter synonym SYN_PROC_SYN_068_001 owner to syn005;
--修改为不存在的属主：报错
drop user if exists test_syn05;
alter synonym SYN_PROC_SYN_068_001 owner to test_syn05;
--修改为存在的属主：新属主有create权限
GRANT ALL PRIVILEGES TO syn005;
alter synonym syn_fun_syn_068_001 owner to syn005;
--清理数据
drop user if exists syn005 cascade;
drop synonym if exists syn_fun_syn_068_001 cascade;
drop procedure if exists SYN_PEOC_068_001;
drop function if exists SYN_FUN_068_001(c int);