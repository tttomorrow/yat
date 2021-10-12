-- @testpoint: 所有输入都是相同的类型，并且不是unknown类型，解析成这种类型

-- @testpoint:所有输入都是相同的类型，并且不是unknown类型进行union：success
explain performance SELECT 123::int union SELECT 456::int;
explain performance SELECT 123.456::float8 union SELECT 456.123::float8 union SELECT 789.123::float8;
explain performance SELECT 123.456::REAL union SELECT 456.123::REAL union SELECT 789.123::REAL;
explain performance SELECT 123::text union SELECT 456::text;
explain performance SELECT 123::clob union SELECT 456::clob;
explain performance SELECT 'test29'::name union SELECT 'test29'::name;
explain performance SELECT '2020-09-28'::date union SELECT '2020-09-30'::date;
explain performance SELECT HEXTORAW('DEADBEEF')::raw union SELECT HEXTORAW('DEABEEF')::raw;
explain performance SELECT 'fat & rat'::tsquery union SELECT 'sate & rat'::tsquery;
explain performance SELECT inet '0.0.0.0/24'::inet union SELECT inet '0.0.0.0/24'::inet;
explain performance SELECT B'1'::bit union SELECT B'101'::bit(3);

--清理环境
--no need to clean