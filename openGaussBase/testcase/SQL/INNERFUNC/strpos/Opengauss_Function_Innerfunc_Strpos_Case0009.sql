-- @testpoint: substring不在string字符中，返回结果为0
-- @description: strpos(string, substring),指定的子字符串的位置

select strpos('source', 'wc');
select strpos('wc', 'source');
select strpos('source', '2');