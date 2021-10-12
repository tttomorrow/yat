-- @testpoint: split_part多参或少参，合理报错
-- @description: split_part(string text, delimiter text, field int),根据delimiter分隔string返回生成的第field个子字符串

select split_part('abc~@~def~@~ghi', 'abc','~@~', 2);
select split_part('abc~@~def~@~ghi', 2);
select split_part('abc~@~def~@~ghi','~@~');