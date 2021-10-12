--  @testpoint:函数参数名有效值测试，以小写字母开头
 CREATE OR REPLACE FUNCTION func_increment1(test_func1 integer) RETURNS integer AS $$
        BEGIN
                RETURN test_func1 + 1;
        END;
$$ LANGUAGE plpgsql;
/
select proargnames from pg_proc where proname='func_increment1';
call func_increment1(2);
drop FUNCTION func_increment1;