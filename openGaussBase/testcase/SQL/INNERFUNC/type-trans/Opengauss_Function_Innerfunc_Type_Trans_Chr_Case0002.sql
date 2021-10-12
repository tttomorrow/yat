-- @testpoint: 类型转换函数to_char (string)将char、varchar、varchar2、clob类型转换为varchar类型，合理报错

-- char转换为varchar
select char_length(to_char(lpad('abccc',1024*1024*10,'x')::char(10485761)));

-- varchar2转换为varchar
select char_length(to_char(lpad('abccc',1024*1024*11,'x')::varchar2(10485761)));
