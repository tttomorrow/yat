-- @testpoint: 自然对数lnx输入为特殊字符/字母/非隐式字符串,合理报错
SELECT LN(r);
SELECT LN(~);
SELECT LN('a');
