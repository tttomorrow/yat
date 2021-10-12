--  @testpoint:创建函数指定参数数据类型是字符类型，不带精度
drop FUNCTION if EXISTS y_testfun3;
CREATE FUNCTION y_testfun3 (c_VARCHAR2 VARCHAR2,c_NVARCHAR2 NVARCHAR2,c_CLOB CLOB,c_TEXT TEXT) RETURNS VARCHAR2  AS $$
        BEGIN
                RETURN (c_VARCHAR2,c_NVARCHAR2,c_CLOB,c_TEXT);
        END;
$$ LANGUAGE plpgsql;
/

call y_testfun3('abc','hello world','beautiful','what');
drop FUNCTION y_testfun3;


--创建函数指定参数数据类型是字符类型，带精度(根据开发者指南描述不进行精度检测)

drop FUNCTION if EXISTS y_testfun4;
CREATE FUNCTION y_testfun4 (c_VARCHAR2 VARCHAR2(10),c_NVARCHAR2 NVARCHAR2(10)) RETURNS VARCHAR2  AS $$
        BEGIN
                RETURN (c_VARCHAR2,c_NVARCHAR2);
        END;
$$ LANGUAGE plpgsql;
/

call y_testfun4('abc','hello world');
drop FUNCTION y_testfun4;