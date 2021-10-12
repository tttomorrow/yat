-- @testpoint: 测试存储过程中if条件结果为字符串（'true','false'）

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_IF_ELSE_009
AS
begin
	begin
		if('true')
		then
			raise info 'The condition is true';
		end if;
	end;
	begin
		if('false')
		then
			raise info 'The condition is false';
		end if;
	end;
end;
/
--调用存储过程
Call PROC_IF_ELSE_009();

--清理环境
drop PROCEDURE PROC_IF_ELSE_009;