-- @testpoint: 测试存储过程中嵌套if/else判断的if/else判断语句

--创建存储过程
CREATE OR REPLACE PROCEDURE PROC_IF_ELSE_013
AS
  v_bool boolean;
  v_bool_flag boolean;
begin
	begin    
		v_bool:=true;
		if(v_bool='1')
		then
			raise info 'The condition 1 is true';
		elsif(v_bool='TRUE')
		then
			raise info 'The condition TRUE is true';
		elsif(v_bool='T')
		then
			raise info 'The condition T is true';
		else
			raise info 'The condition is true';
		end if;
	end;
	begin    
		v_bool_flag:=true;
		if(v_bool_flag='1')
		then
			raise info 'The condition 1 is true';
			if(v_bool_flag='TRUE')
			then
				raise info 'The condition TRUE is true';
				if(v_bool_flag='T')
				then
					raise info 'The condition T is true';
					v_bool_flag:=false;
					if(v_bool_flag='0')
					then                
						raise info 'The condition 0 is true';
						if(v_bool_flag='FALSE')
						then
							raise info 'The condition FALSE is true';
							if(v_bool_flag='F')
							then
								raise info 'The condition F is true';
								case v_bool_flag
								when '1' then
									raise info 'The condition 1 is true';
								when 'TRUE' then
									raise info 'The condition TRUE is true';
								when 'T' then
									raise info 'The condition T is true';
								when 'F' then
									raise info 'The condition F is true';
								when 'FALSE' then
								raise info 'The condition FALSE is true';
								when '0' then
									raise info 'The condition 0 is true';
								else
									raise info 'The condition XXXX is false';
								end case;
							end if;
						end if;
					end if;
				end if;
			end if;
		end if;
	end;
end ;
/


--调用存储过程
Call PROC_IF_ELSE_013();

--清理环境
drop PROCEDURE PROC_IF_ELSE_013;