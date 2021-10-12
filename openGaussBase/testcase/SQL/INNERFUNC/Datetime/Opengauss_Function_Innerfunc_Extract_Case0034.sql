--  @testpoint: ◾将epoch值转换为时间戳的方法不加时区reltime类型负数

SELECT TIMESTAMP WITHOUT TIME ZONE 'epoch' + 720.12 * reltime '-13 months -10 hours' AS RESULT;
SELECT TIMESTAMP WITHOUT TIME ZONE 'epoch' + 1 * reltime '-2 YEARS +5 MONTHS 10 DAYS' AS RESULT;
SELECT TIMESTAMP WITHOUT TIME ZONE 'epoch' + 1.5 * reltime '-365' AS RESULT;
SELECT TIMESTAMP WITHOUT TIME ZONE 'epoch' + 0 * reltime '-12H' AS RESULT;