-- @testpoint: if ...then ...else

create or replace procedure proc_if_else_008(i in integer)
as
    begin
        if i > 0 then
            raise info 'i:% is greater than 0. ',i;
        elsif i < 0 then
            raise info 'i:% is smaller than 0. ',i;
        else
            raise info 'i:% is equal to 0. ',i;
        end if;
        return;
    end;
/

call proc_if_else_008(3);
drop procedure proc_if_else_008;
