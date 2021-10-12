-- @testpoint: 创建函数指定参数数据类型是字符类型，不带精度
drop FUNCTION if EXISTS z_testfun0;
CREATE FUNCTION z_testfun0 (c_CHAR CHAR, c_CHARACTER CHARACTER,c_NCHAR NCHAR) RETURNS CHAR  AS $$
        BEGIN
                RETURN (c_CHAR,c_CHARACTER,c_NCHAR);
        END;
$$ LANGUAGE plpgsql;
/
--proallargtypes字段为空
select proname,proallargtypes from pg_proc where proname='z_testfun0';
--传入精度是1的字符
call z_testfun0('a','b','c');
--传入精度大于1的字符（依然可以调用成功，根据开发者指南描述不进行精度检测）
call z_testfun0('abc','bvd','cde');
drop FUNCTION z_testfun0;

--创建函数指定参数数据类型是字符类型，带精度（根据开发者指南描述不进行精度检测）
drop FUNCTION if EXISTS y_testfun0;
CREATE FUNCTION y_testfun0 (c_CHAR CHAR(10),c_CHARACTER CHARACTER(10),c_NCHAR NCHAR(10)) RETURNS CHAR(10)  AS $$
        BEGIN
                RETURN (c_CHAR,c_CHARACTER,c_NCHAR);
        END;
$$ LANGUAGE plpgsql;
/

call y_testfun0 ('you','are','who');
drop FUNCTION y_testfun0;
