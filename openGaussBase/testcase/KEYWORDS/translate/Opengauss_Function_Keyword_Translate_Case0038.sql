--  @testpoint:openGauss关键字translate(非保留),
-- 把在string中包含的任何匹配from中字符的字符转化为对应的在to中的字符，from匹配不到string,to为空


SELECT translate('12345', '@#￥', '');

SELECT translate('12345', '', '');
