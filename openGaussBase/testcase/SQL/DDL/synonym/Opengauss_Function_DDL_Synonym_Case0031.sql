-- @testpoint: 创建同义词时，名称中带英文字符，合理报错
-- @modify at: 2020-11-25
--创建函数
drop function if exists SYN_FUN_001(c bigint);
create or replace function SYN_FUN_001(c bigint) return int
as
b int := c;
begin
	for i in 1..c loop
		b:= b - 1;
	end loop;
	return b;
end;
/
--创建函数的同义词
create or replace synonym 1 for SYN_FUN_001;
create or replace synonym acd* for SYN_FUN_001;
create or replace synonym acd+ for SYN_FUN_001;
create or replace synonym acd- for SYN_FUN_001;
create or replace synonym acd/ for SYN_FUN_001;
create or replace synonym acd\ for SYN_FUN_001;
create or replace synonym acd% for SYN_FUN_001;
create or replace synonym acd! for SYN_FUN_001;
create or replace synonym acd@ for SYN_FUN_001;
create or replace synonym acd^ for SYN_FUN_001;
create or replace synonym acd( for SYN_FUN_001;
create or replace synonym acd) for SYN_FUN_001;
create or replace synonym acd~ for SYN_FUN_001;
create or replace synonym acd< for SYN_FUN_001;
create or replace synonym acd> for SYN_FUN_001;
create or replace synonym acd| for SYN_FUN_001;
create or replace synonym acd. for SYN_FUN_001;
create or replace synonym acd= for SYN_FUN_001;
create or replace synonym acd{ for SYN_FUN_001;
create or replace synonym acd} for SYN_FUN_001;
--清理环境
drop function if exists SYN_FUN_001(c bigint) cascade;
