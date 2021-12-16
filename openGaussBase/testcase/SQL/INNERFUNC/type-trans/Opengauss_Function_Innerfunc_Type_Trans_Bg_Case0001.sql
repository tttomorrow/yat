-- @testpoint: 类型转换函数to_bigint，入参为有效值时（边界值、正、负数）

select to_bigint('0');

select to_bigint('123364545554455');

select to_bigint('-123364545554455');

select to_bigint('9223372036854775807');

select to_bigint('-9223372036854775808');

select to_bigint('123364545554455'::varchar(10));

select to_bigint('123364545554455'::varchar(30));