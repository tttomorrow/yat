-- @testpoint: 条件语句 if ...then ...else

create or replace procedure proc_if_else_002
as
begin
    if(false)
    then
        raise info 'the condition is true';
    else
        raise info 'the condition is false';
    end if;
end ;
/
call proc_if_else_002();
drop procedure proc_if_else_002;





