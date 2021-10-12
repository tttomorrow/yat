-- @testpoint: 时间和日期操作符+，date与没有明确类型的字符串相加，合理报错
SELECT date '2001-10-01' - '7' AS RESULT;