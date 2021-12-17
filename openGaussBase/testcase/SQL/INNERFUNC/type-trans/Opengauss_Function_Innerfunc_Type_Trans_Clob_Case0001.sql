-- @testpoint: 类型转换函数to_clob(char/nchar/varchar/varchar2/nvarchar2/text/raw)，入参为有效值

select to_char('01110');
-- char转换为to_clob
select to_clob('hello111'::char(15));
select to_clob('123456789'::char);
select to_clob('123456789'::char(5));
select to_clob('123456789'::char(77));
select char_length(to_clob(lpad('abccc',1024*1024*10,'x')::char(10485760)));

-- nchar转换为to_clob
select to_clob('hello123'::nchar(10));
select char_length(to_clob(lpad('abccc',1024*1024*10,'x')::nchar(10485760)));

-- varchar转换为to_clob
select to_clob('hello234'::varchar(10));
select char_length(to_clob(lpad('abccc',1024*1024*10,'x')::varchar(10485760)));

-- varchar2转换为to_clob
select to_clob('hello345'::varchar2(10));
select to_clob('123456789'::varchar2);
select to_clob('123456789'::varchar2(5));
select to_clob('123456789'::varchar2(77));
select char_length(to_clob(lpad('abccc',1024*1024*10,'x')::varchar2(10485760)));
select char_length(to_clob(lpad('hi', 12, 'xyza')::varchar2(500)));

-- nvarchar2转换为to_clob
select to_clob('hello456'::nvarchar2(10));

-- text转换为to_clob
select to_clob('world222!'::text);

-- raw
select to_clob('aa'::raw);
select to_clob('aaa'::raw);
select to_clob('abcdef'::raw(10));
select to_clob('5d'::raw(10));
select char_length(to_clob(lpad('a',12,'b')::raw));