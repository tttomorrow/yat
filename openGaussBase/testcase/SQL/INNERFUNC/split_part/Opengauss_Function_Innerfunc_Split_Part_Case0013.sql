-- @testpoint: delimiter为有效字符串
-- @description: split_part(string text, delimiter text, field int),根据delimiter分隔string返回生成的第field个子字符串

select split_part('abc~@~def~@~ghi', '~@~', 2);
select split_part('abc~@~def~@~ghi', 'def', 1);
select split_part('abc~@~def~@~ghi', 'ghi', 2);