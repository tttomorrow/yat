-- @testpoint: cast用例,部分用例合理报错
-- 不符合规则money类型参与转换
select cast('$2'::money as unsigned);
select cast('$2' money as unsigned);
select cast('$2':money as unsigned);
select cast('$2' as unsigned);
select cast('&2'::money as unsigned);
select cast('$2-$1'::money as unsigned);
