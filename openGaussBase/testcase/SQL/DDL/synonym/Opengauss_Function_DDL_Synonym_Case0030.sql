-- @testpoint: 同一个函数的多个同义词同时使用
-- @modify at: 2020-11-25
--创建函数
drop function if exists SYN_FUN_001(a int,str varchar) cascade;
create or replace function SYN_FUN_001(a int,str varchar) return varchar
as
	cur sys_refcursor;
	var varchar(1024);
	new_var varchar(1024):=str;
begin
	open cur for select str from sys_dummy;
	for i in 1..a loop
		fetch cur into var;
		exit when cur%notfound;
		new_var:=new_var||var;
	end loop;
	return new_var;
end;
/
--创建多个函数的同义词
create or replace synonym SYN_FUN_SYN_001 for SYN_FUN_001;
create or replace synonym SYN_FUN_SYN_002 for SYN_FUN_001;
create or replace synonym SYN_FUN_SYN_003 for SYN_FUN_001;
create or replace synonym SYN_FUN_SYN_004 for SYN_FUN_001;
create or replace synonym SYN_FUN_SYN_005 for SYN_FUN_001;
create or replace synonym SYN_FUN_SYN_006 for SYN_FUN_001;
create or replace synonym SYN_FUN_SYN_007 for SYN_FUN_001;
create or replace synonym SYN_FUN_SYN_008 for SYN_FUN_001;
create or replace synonym SYN_FUN_SYN_009 for SYN_FUN_001;
create or replace synonym SYN_FUN_SYN_010 for SYN_FUN_001;
--查询
select SYN_FUN_SYN_001(1,SYN_FUN_SYN_002(2,SYN_FUN_SYN_003(3,SYN_FUN_SYN_004
(4,SYN_FUN_SYN_005(5,SYN_FUN_SYN_006(6,SYN_FUN_SYN_007(7,SYN_FUN_SYN_008
(8,SYN_FUN_SYN_009(9,SYN_FUN_SYN_010(10,'a')))))))))) from sys_dummy;
--清理环境
drop function if exists SYN_FUN_001(a int,str varchar) cascade;
drop synonym SYN_FUN_SYN_001;
drop synonym SYN_FUN_SYN_002;
drop synonym SYN_FUN_SYN_003;
drop synonym SYN_FUN_SYN_004;
drop synonym SYN_FUN_SYN_005;
drop synonym SYN_FUN_SYN_006;
drop synonym SYN_FUN_SYN_007;
drop synonym SYN_FUN_SYN_008;
drop synonym SYN_FUN_SYN_009;
drop synonym SYN_FUN_SYN_010;