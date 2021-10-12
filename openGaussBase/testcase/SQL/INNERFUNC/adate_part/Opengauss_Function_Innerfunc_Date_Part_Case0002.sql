-- @testpoint: 描述：获取月份的值。如果大于12，则取与12的模。等效于extract(field from timestamp)。返回值类型：double precision

SELECT date_part('month', interval '2 years 3 months') from sys_dummy;