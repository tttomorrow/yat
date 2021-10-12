-- @testpoint: 输入为特殊字符/字母/非隐式字符串,合理报错


select asin('Infinity');
select asin('~');
select asin('a');