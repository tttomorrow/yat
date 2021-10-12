--  @testpoint:创建函数，指定参数是OUT模式，添加returns子句，返回数据类型与出参定义的数据类型一致
drop FUNCTION if EXISTS x1_testfun;
CREATE FUNCTION x1_testfun (c_int  OUT int   ) returns int   AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/

call x1_testfun(999);
drop FUNCTION x1_testfun;