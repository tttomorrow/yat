-- @testpoint: 自定义函数同义词在存储过程中调用
-- @modify at: 2020-11-25
--创建自定义函数
drop function if exists SYN_FUN_001(ARRAY_C integer[]) cascade;
create  function SYN_FUN_001(ARRAY_C integer[]) return integer[]
as
ARRAY_A integer[];
begin
	ARRAY_A:=ARRAY_C;
	return ARRAY_A;
end;
/
--创建自定义函数的同义词
drop synonym if exists SYN_FUN_SYN_001;
create  synonym SYN_FUN_SYN_001 for SYN_FUN_001;
--创建存储过程调用自定义函数的同义词
drop procedure if exists SYN_PEOC_001;
create  procedure SYN_PEOC_001 (ARRAY_A integer[] )
as
begin
    raise info '%',SYN_FUN_SYN_001(ARRAY_A);
end;
/
--调用存储过程
select SYN_PEOC_001(SYN_FUN_SYN_001(array[1,2,3,4,5,6,7,8,9,10]));
--清理环境
drop function if exists SYN_FUN_001(ARRAY_C integer[]) cascade;
drop procedure if exists SYN_PEOC_001;
drop synonym if exists SYN_FUN_SYN_001;
