-- @testpoint: convert_to_nocase(text, text)将字符串转换为指定的编码类型，入参为无效值时合理报错

select convert_to_nocase('aaa', 'ascii');
select convert_to_nocase('你好$%^*', 'unicode1');
select convert_to_nocase('你好', 'utf-8','999');
select convert_to_nocase('你好');
select convert_to_nocase(false, 'latin1');