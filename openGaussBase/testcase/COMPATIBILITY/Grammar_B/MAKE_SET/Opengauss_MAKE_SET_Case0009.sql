-- @testpoint:bits不输入单引号且不输入值时make_set的运算,部分测试用例合理报错
select make_set(,'a','b','c','d');

-- bits不输入单引号且不输入值时make_set的运算
select make_set('','a','b','c','d');
