--  @testpoint: ◾将epoch值转换为时间戳的方法不加时区reltime类型正数

SELECT TIMESTAMP WITHOUT TIME ZONE 'epoch' + 720.12 * reltime '60' AS RESULT;
SELECT TIMESTAMP WITHOUT TIME ZONE 'epoch' + 1 * reltime '31.25' AS RESULT;
SELECT TIMESTAMP WITHOUT TIME ZONE 'epoch' + 1.5 * reltime '1 years 1 mons 8 days 12:00:00' AS RESULT;
SELECT TIMESTAMP WITHOUT TIME ZONE 'epoch' + 0 * reltime 'P-1.1Y10M' AS RESULT;