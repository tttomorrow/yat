-- @testpoint: 隐式转换关系，结合union，不是同一类型合理报错

-- @testpoint:输入类型是同一个类型范畴，则选择该类型范畴的首选类型 union：success
explain performance SELECT 123::int union SELECT 456::int;
explain performance SELECT '2020-09-30'::varchar union SELECT '2020-09-29'::date;
explain performance SELECT HEXTORAW('DEADBEEF')::blob union SELECT HEXTORAW('DEABEEF')::raw;

--清理环境
--no need to clean