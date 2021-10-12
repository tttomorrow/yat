-- @testpoint: 测试存储过程中if条件结果为0、1.

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_IF_ELSE_0008
AS
begin
	begin
		if('0')
		then
			raise info 'The condition is true';
		else
			raise info 'The condition is false';
		end if;
	end;
	begin
		if('1')
		then
			raise info 'The condition is true';
		else
			raise info 'The condition is false';
		end if;
	end;
end ;
/
--调用存储过程
Call PROC_IF_ELSE_0008();

--清理环境
drop PROCEDURE PROC_IF_ELSE_0008;
