--  @testpoint: ◾将epoch值转换为时间戳的方法不加时区带每个时间段单位

SELECT TIMESTAMP WITHOUT TIME ZONE 'epoch' + 1 * INTERVAL '1 year 1 month 30day 24h 60m 60s' AS RESULT;