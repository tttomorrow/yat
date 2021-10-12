--  @testpoint:openGauss关键字translate(非保留),
-- 把在string中包含的任何匹配from中字符的字符转化为对应的在to中的字符，from匹配到string,to为空

--from长度不为空，to长度为空函数执行成功

SELECT translate('12345', '12345', '');
--from长度为空，to长度为空函数执行成功

SELECT translate('', '', '');

--from长度小于strin
SELECT translate('12345', '125', '');
