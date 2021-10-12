-- @testpoint: delimiter为null
-- @description: split_part(string text, delimiter text, field int),根据delimiter分隔string返回生成的第field个子字符串

select split_part('abc~@~def~@~ghi', null, 2);
select split_part('abc~@~def~@~ghi', '', 2);