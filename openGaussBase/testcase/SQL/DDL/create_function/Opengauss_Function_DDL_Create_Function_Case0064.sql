--  @testpoint:创建函数指定参数数据类型是字符类型，不带精度
drop FUNCTION if EXISTS y_testfun1;
CREATE FUNCTION y_testfun1 (c_VARCHAR VARCHAR,c_CHARACTER_VARYING CHARACTER VARYING ) RETURNS VARCHAR  AS $$
        BEGIN
                RETURN (c_VARCHAR,c_CHARACTER_VARYING);
        END;
$$ LANGUAGE plpgsql;
/
call y_testfun1 ('you','are');
drop FUNCTION  y_testfun1;

--创建函数指定参数数据类型是字符类型，带精度(根据开发者指南描述不进行精度检测)
drop FUNCTION if EXISTS y_testfun2;
CREATE FUNCTION y_testfun2 (c_VARCHAR VARCHAR(10),c_CHARACTER_VARYING CHARACTER VARYING(10) ) RETURNS VARCHAR  AS $$
        BEGIN
                RETURN (c_VARCHAR,c_CHARACTER_VARYING);
        END;
$$ LANGUAGE plpgsql;
/

call y_testfun2 ('you','are');
drop FUNCTION  y_testfun2;