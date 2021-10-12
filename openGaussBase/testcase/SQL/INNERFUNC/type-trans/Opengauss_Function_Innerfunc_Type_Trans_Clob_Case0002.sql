-- @testpoint: to_clob函数异常校验，合理报错

-- char
SELECT to_clob('hello111'::CHAR(h));

-- NCHAR
SELECT to_clob('gauss123'::NCHAR(*));
SELECT char_length(to_clob(lpad('abcCC',1024*1024*10,'x')::NCHAR(10485761)));

-- VARCHAR
SELECT to_clob('gauss234'::VARCHAR(  ));

-- varchar2
SELECT to_clob('gauss345'::VARCHAR2(1#0));
SELECT char_length(to_clob(lpad('abcCC',1024*1024*10,'x')::varchar2(10485761)));

-- NVARCHAR2
SELECT to_clob('gauss456'::NVARCHAR2(￥%));
SELECT char_length(to_clob(lpad('a',11*1024*1024,'b')::NVARCHAR2(10485761)));

-- text
SELECT to_clob('World222!'::TEXT(ni));

-- raw
SELECT to_clob('ABCDEFg'::RAW(10));
SELECT to_clob(0x5d::RAW(10));
SELECT char_length(to_clob(lpad('a',12,'x')::RAW));
