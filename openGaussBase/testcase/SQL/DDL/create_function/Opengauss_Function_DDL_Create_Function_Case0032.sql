--  @testpoint:一个函数存在两个同名的参数,合理报错
drop function if exists c_test1(arg1 int4,arg1 int4);
CREATE FUNCTION c_test1(arg1 int4,arg1 int4) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
 /