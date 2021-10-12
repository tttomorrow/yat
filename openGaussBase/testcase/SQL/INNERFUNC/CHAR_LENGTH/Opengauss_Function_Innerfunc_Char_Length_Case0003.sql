-- @testpoint: char_length函数入参给不加单引号的字符串
select char_length($$jjslf$$);
select char_length($$jj' 'slf$$);
