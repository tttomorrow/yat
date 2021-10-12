-- @testpoint: opengauss比较操作符=，隐式转换的类型比较

-- 可以隐式转换的不同类型间比较
select '123'::CHAR = '125'::VARCHAR2 as result;
select '125'::CHAR = '125'::VARCHAR2 as result;
select '126'::CHAR = '125'::VARCHAR2 as result;
select '012'::CHAR = '125'::VARCHAR2 as result;
select '2129'::CHAR = '125'::VARCHAR2 as result;
select '1129'::CHAR = '125'::VARCHAR2 as result;
select '123'::CHAR = '125'::NUMBER as result;
select '16'::CHAR = '10'::RAW as result;
select '17'::CHAR = '10'::RAW as result;
select '123'::CHAR = '125'::CLOB as result;
select '123'::VARCHAR2 = '123'::CHAR as result;
select '123'::VARCHAR2 = '123'::NUMBER as result;
select '123'::VARCHAR2 = '123'::CLOB as result;
select '123'::NUMBER = '123'::CHAR as result;
select '123'::NUMBER = '123'::VARCHAR2 as result;
select '123'::RAW = '123'::CHAR as result;
select '123'::RAW = '123'::VARCHAR2 as result;
select '123'::CLOB = '123'::CHAR as result;
select '123'::CLOB = '123'::VARCHAR2 as result;
select '123'::CLOB = '123'::NUMBER as result;
select '123'::INT4 = '123'::CHAR as result;
select '123'::INT4 = '1'::BOOLEAN as result;
select '1'::BOOLEAN = '123'::INT4 as result;
select '2001-09-28'::VARCHAR2 = '2001-09-27'::DATE as result;
select '2001-09-28'::DATE = '2001-09-28'::VARCHAR2 as result;