--  @testpoint:创建函数，指定参数是INOUT模式，添加returns子句，返回数据类型与出参定义的数据类型一致
drop FUNCTION if EXISTS x2_testfun;
CREATE FUNCTION x2_testfun (c_int INOUT int   ) returns text   AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/

call x2_testfun(8);
drop FUNCTION x2_testfun;