--  @testpoint:函数参数名有效值测试，以下划线开头
drop FUNCTION if EXISTS func_increment2(_tfunc1 integer);
CREATE OR REPLACE FUNCTION func_increment2(_tfunc1 integer) RETURNS integer AS $$
        BEGIN
                RETURN _tfunc1 + 1;
        END;
$$ LANGUAGE plpgsql;
/
select proargnames from pg_proc where proname='func_increment2';
drop FUNCTION func_increment2;