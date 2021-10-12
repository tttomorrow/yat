-- @testpoint: string和substring均为有效值
-- @description: strpos(string, substring),指定的子字符串的位置

select strpos('source', 'rc');
select strpos('hello', 'o');
select strpos('asdfghjkl,zxcvbnm', ',');
select strpos('@#$%^&*()$%', '%');