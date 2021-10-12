-- @testpoint: 测试存储过程中if判断条件为非运算

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_IF_ELSE_010
AS
begin
	begin
		if(NOt FAlse)
		then
			raise info 'The condition is true';
		else
			raise info 'The condition is false';
		end if;
	end;
	begin
		if(NOT(NOT(Not(NOT(NOt(NOT(NOT(Not(NOT(NOt (NOt FAlse)))))))))))
		then
			raise info 'The condition is true';
		else
			raise info 'The condition is false';
		end if;
	end;
end ;
/
--调用存储过程
Call PROC_IF_ELSE_010();

--清理环境
drop PROCEDURE PROC_IF_ELSE_010;
