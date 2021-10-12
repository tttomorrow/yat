-- @testpoint:  输入空值
select left('',1);
select left(null,1);
select left('abc','');
select left('abc',null);