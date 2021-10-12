--  @testpoint:只有一个参数，指定参数模式为INOUT
DROP FUNCTION if EXISTS k_testfun1 (arg1 INOUT integer);
CREATE  FUNCTION k_testfun1 (arg1 INOUT integer) RETURNS integer AS $$
        BEGIN
                RETURN arg1 + 1;
        END;
$$ LANGUAGE plpgsql;
/
--查询pg_proc表proargmodes字段是b,即表示参数arg1是INOUT参数模式
select proargmodes from pg_proc where proname='k_testfun1';
drop function  k_testfun1;