-- @testpoint: char_length函数合法值校验
select char_length('jjslf');
select char_length('jj          slf');
select char_length('jj''slf');
select char_length('jjslf'::text);
select char_length(123.45);
