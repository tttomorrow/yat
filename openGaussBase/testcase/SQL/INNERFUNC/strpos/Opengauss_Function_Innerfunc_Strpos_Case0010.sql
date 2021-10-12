-- @testpoint: substring为空值
-- @description: strpos(string, substring),指定的子字符串的位置

select strpos('source', null);
select strpos('source', '');