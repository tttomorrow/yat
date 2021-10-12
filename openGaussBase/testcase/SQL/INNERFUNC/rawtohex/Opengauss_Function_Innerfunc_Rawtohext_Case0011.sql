-- @testpoint: rawtohex函数进行大量字符串的转换 
select rawtohex(to_char(LPAD('a',800,'a'))||to_char(LPAD('a',800,'a')));