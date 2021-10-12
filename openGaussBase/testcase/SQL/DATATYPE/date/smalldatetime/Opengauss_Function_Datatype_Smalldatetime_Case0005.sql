-- @testpoint: 结合case when对smalldatetime日期类型进行比较

SELECT CASE WHEN smalldatetime '2018-09-17 11:22:33.456' > smalldatetime '2018-09-16 11:22:33.456' THEN 'A' ELSE 'B' END;