--  @testpoint:函数参数个数测试，参数个数15个，创建成功

    drop FUNCTION if EXISTS f_func1();

    CREATE FUNCTION f_func1( arg1 int4, arg2 int4,arg3 int4,arg4 int4,arg5 int4,arg6 int4,arg7 int4,arg8 int4,arg9 int4,arg10 int4,arg11 int4,arg12 int,arg13 int4,arg14 int4,arg15 int4) RETURNS int4
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
   /
    select proargnames from pg_proc where proname='f_func1';
    drop FUNCTION f_func1;