-- @testpoint: 测试存储过程中elsif

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_IF_ELSE_015
AS
  v_int INT;
begin
	begin    
		v_int:=10;
		if((v_int*10+100-90)/10>11)
		then
			raise info '10*10+100-90)/10>11';
		elsif(v_int<(100/10-10+9))
		then
			raise info '10<(100/10-10+9)';
		elsif(v_int>11)
		then
			raise info '10>11';
		else 
			raise info '10<11';
		end if;
	end;
end;
/
--调用存储过程
Call PROC_IF_ELSE_015();

--清理环境
drop PROCEDURE PROC_IF_ELSE_015;