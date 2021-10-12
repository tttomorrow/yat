-- @testpoint: delimiter不在string中,结果返回为空
-- @description: split_part(string text, delimiter text, field int),根据delimiter分隔string返回生成的第field个子字符串

select split_part('abc~@~def~@~ghi', 'adg', 2);
select split_part('abc~@~def~@~ghi', '#$#', 2);