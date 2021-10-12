-- @testpoint: 类型转换函数cast(x as y)函数异常校验，合理报错

-- 时间/日期型
select cast('35-oct-1997' as timestamp with time zone);
select cast('shi' as date);
select cast('10.123000' as timestamp with time zone);

-- 字符型
select cast(interval  as text);
select cast(-125.8 as int1);
select cast('h'::raw as char);

-- 数值类型
select cast('32.5' as tinyint);
select cast('32.0' as smallint);
select cast('-32769' as tinyint);
select cast('hjk' as decimal);
select cast('999.8788' as decimal(3,1));

select cast('7.ghjk' as real);
select cast('@#$$%' as double precision);

-- 布尔型
select cast('1368'::varchar as boolean);
select cast(9::nchar as boolean);
select cast('ok' as boolean);
select cast('pass'::clob as boolean);