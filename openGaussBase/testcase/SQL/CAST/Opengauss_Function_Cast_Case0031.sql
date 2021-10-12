-- @testpoint: 输入类型是同一个类型范畴，则选择该类型范畴的首选类型

-- @testpoint:输入类型是同一个类型范畴，则选择该类型范畴的首选类型 union：success
explain performance SELECT 123::int2 union SELECT 456::float8;
explain performance SELECT 123.456::float8 union SELECT 456.123::int union SELECT 789.123::NUMBER;
explain performance SELECT 123.456::DOUBLE PRECISION union SELECT 456.123::NUMBER union SELECT 789.123::REAL;
explain performance SELECT 123::clob union SELECT 456::text;
explain performance SELECT '2020-09-28'::date union SELECT '2020-09-30'::timestamp;
explain performance SELECT HEXTORAW('DEADBEEF')::BLOB union SELECT HEXTORAW('DEABEEF')::raw;
explain performance SELECT inet '0.0.0.0/24'::inet union SELECT inet '0.0.0.0/24'::cidr;
explain performance SELECT B'1'::bit varying union SELECT B'101'::bit(3);

--清理环境
--no need to clean