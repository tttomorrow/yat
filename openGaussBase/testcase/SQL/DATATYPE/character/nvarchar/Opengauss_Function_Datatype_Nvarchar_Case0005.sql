-- @testpoint: NVARCHAR(n)内建函数测试

--step1:指定类型的内建函数; expect:成功
select to_clob('test'::nvarchar);
select datalength('test'::nvarchar);

--step2:一般字符类型函数; expect:成功
--字符串中的字符个数
select char_length('hello'::nvarchar);
select character_length('hello'::nvarchar);
--获取指定字符串的字节数
select lengthb('hello'::nvarchar);
--返回字符串的前n个字符。当n是负数时，返回除最后|n|个字符以外的所有字符
select left('abcde'::nvarchar, 2);
--通过填充字符fill（缺省时为空白），把string填充为length长度。如果string已经比length长则将其尾部截断
select lpad('nvarchar', 10, 'a');
--返回适用于在sql语句里当作文本使用的形式（使用适当的引号进行界定）
select quote_literal('nvarchar'::nvarchar);
--正则表达式的模式匹配函数
select regexp_like('nvarchar'::nvarchar,'[var]');
--将string重复number次
select repeat('nvarchar'::nvarchar, 3);
--把字符串string里出现地所有子字符串from的内容替换成子字符串to的内容
select replace('nvarchar'::nvarchar, 'a', 'x');
--使用填充字符fill（缺省时为空白），把string填充到length长度。如果string已经比length长则将其从尾部截断
select rpad('nvarchar'::nvarchar, 5, 'xy');
select rpad('n'::nvarchar, 5, 'xy');
--连接字符串和非字符串
select 'nvarchar'::nvarchar||42 as result;
--获取参数string中字符的数目
select length('nvarchar'::nvarchar);
--把字符串转化为大写
select upper('nvarchar'::nvarchar);
--把字符串转化为小写
select lower('NVARCHAR'::nvarchar);
--参数string的第一个字符的ASCII码
select ascii('nvarchar'::nvarchar);