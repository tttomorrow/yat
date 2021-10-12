-- @testpoint: char_length函数入参异常校验，合理报错
select char_length(null);
select char_length('');
select char_length();
select char_length('jjslf','jdflsjf');
