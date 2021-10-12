-- @testpoint: 测试存储过程返回值类型——boolean

--创建存储过程
create or replace procedure proc_return_value_013(p1 bool)  as
begin
    if(p1)
    then
		raise info 'the condition is %',p1;
    else
        raise info 'the condition is %',p1;
    end if;
end;
/
--调用存储过程
call proc_return_value_013(true);
call proc_return_value_013(false);
call proc_return_value_013(true);
call proc_return_value_013(false);
call proc_return_value_013('t');
call proc_return_value_013('f');
call proc_return_value_013('t');
call proc_return_value_013('f');
call proc_return_value_013(1);
call proc_return_value_013(0);
--清理环境
drop procedure proc_return_value_013;

