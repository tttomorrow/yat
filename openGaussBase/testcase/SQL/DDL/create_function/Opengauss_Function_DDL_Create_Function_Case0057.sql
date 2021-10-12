-- @testpoint: 创建函数指定参数的数据类型，遍历整数类型，超过TINYINT上限255，合理报错
DROP FUNCTION if EXISTS k_testfun9 (c_TINYINT TINYINT,c_SMALLINT SMALLINT,c_INTEGER INTEGER,c_BINARY_INTEGER BINARY_INTEGER,c_BIGINT BIGINT);
CREATE  FUNCTION k_testfun9 (c_TINYINT TINYINT,c_SMALLINT SMALLINT,c_INTEGER INTEGER,c_BINARY_INTEGER BINARY_INTEGER,c_BIGINT BIGINT) RETURNS int1 AS $$
        BEGIN
                RETURN c_TINYINT + c_SMALLINT+c_INTEGER+c_BINARY_INTEGER+c_BIGINT;
        END;
$$ LANGUAGE plpgsql;
/
--proallargtypes字段是空
select proname,proallargtypes from pg_proc where proname='k_testfun9';
--超过TINYINT上限255，合理报错
call k_testfun9(100,100,10,10,36);
drop function  k_testfun9;