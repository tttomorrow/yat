-- @testpoint: cast用例,部分用例合理报错,部分用例合理报错
-- 设置时区
set time zone 'uct';
-- 不符合规则的timestamp类型参与转换
select cast('2022-11-10 18:03:20'::timestamp as unsigned);
select cast('2022-11-10'::timestamp as unsigned);
select cast('18:03:20'::timestamp as unsigned);
select cast('2022-11-10 18:03:20' timestamp as unsigned);
select cast('2022-11-10 18:03:20':timestamp as unsigned);
select cast('20221219'::timestamp as unsigned);
select cast('20221219-02-09'::timestamp as unsigned);
select cast('20221219-02+09'::timestamp as unsigned);
select cast('2022-11-10 18:03:20' as unsigned);
select cast('$34'::timestamp as unsigned);
