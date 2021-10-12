-- @testpoint: 存储过程使用goto 语句，不支持 合理报错

create or replace procedure proc_case_branch(pi_result in integer, pi_return out integer)
as
    begin
    goto pos1;
        case pi_result
            when 1
     <<pos1>>
            then
                pi_return := 111;
            else
                pi_return := 000;
        end case;
        raise info 'pi_return : %',pi_return ;
end;
/
call proc_case_branch(1,0);
drop procedure proc_case_branch;

