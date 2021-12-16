-- @testpoint: 类型转换函数to_char (string)将char、varchar、varchar2、clob类型转换为varchar类型，

select to_char('01110');
-- char转换为varchar
select to_char('123456789'::char);
select to_char('123456789'::char(5));
select to_char('123456789'::char(77));
select char_length(to_char(lpad('abccc',1024*1024*10,'x')::char(10485760)));
select char_length(to_char(lpad('abccc',1024*1024*11,'x')::char(10485760)));

-- varchar2转换为varchar
select to_char('123456789'::varchar2);
select to_char('123456789'::varchar2(5));
select to_char('123456789'::varchar2(77));
select char_length(to_char(lpad('abccc',1024*1024*10,'x')::varchar2(10485760)));

-- clob转换为varchar
select to_char('123456789'::clob);
select char_length(to_char(lpad('abccc',1024*1024*10,'x')::clob));
