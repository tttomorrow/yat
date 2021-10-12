--  @testpoint:修改函数权限
drop FUNCTION if EXISTS v_testfun6(c_int int);
CREATE FUNCTION v_testfun6 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
STRICT;
/

--修改函数权限是SECURITY INVOKER
alter function v_testfun6 (c_int int) SECURITY INVOKER;
--修改函数权限是AUTHID CURRENT_USER
alter function v_testfun6 (c_int int) AUTHID CURRENT_USER;
--修改函数权限是SECURITY DEFINER
alter function v_testfun6 (c_int int) SECURITY DEFINER;
--改函数权限是AUTHID DEFINER
alter function v_testfun6 (c_int int) AUTHID DEFINER;

drop function  v_testfun6(c_int int);