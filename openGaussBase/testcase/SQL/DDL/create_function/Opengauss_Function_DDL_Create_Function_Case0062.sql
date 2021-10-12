--  @testpoint:创建函数指定参数数据类型是布尔类型

drop FUNCTION if EXISTS z_testfun1;
CREATE FUNCTION z_testfun1 (c_BOOLEAN  BOOLEAN) RETURNS BOOLEAN  AS $$
        BEGIN
                RETURN c_BOOLEAN;
        END;
$$ LANGUAGE plpgsql;
/
call z_testfun1('y');
call z_testfun1('true');
call z_testfun1('TRUE');
call z_testfun1('t');
call z_testfun1('YES');
call z_testfun1(1);
call z_testfun1(3);

--调用函数，boolean值为假
call z_testfun1('FALSE');
call z_testfun1('false');
call z_testfun1(0);
call z_testfun1('n');
call z_testfun1('no');
call z_testfun1(-1);
call z_testfun1(null);

drop FUNCTION z_testfun1;