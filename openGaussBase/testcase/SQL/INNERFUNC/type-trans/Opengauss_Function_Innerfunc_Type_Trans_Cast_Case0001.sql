-- @testpoint: 类型转换函数，cast(x as y)将x转换成y指定的类型

-- 时间/日期型
select cast('22-oct-1997' as timestamp with time zone);
select cast('23-jan-2020' as date);
select cast('12-september-10 14:10:10.123000' as timestamp with time zone);

-- 字符型
select cast(interval '15h 2m 12s' as text);
select cast(date 'epoch' as nchar(37));
select cast(2147483648 as varchar);
select cast(-125.8 as char);
select cast('a'::raw as varchar2);

-- 数值类型
select cast('32'::char as tinyint);
select cast('-32'::varchar2 as smallint);
select cast('-32768'::clob as integer);
select cast('2147483648'::text as bigint);

select cast('9' as decimal);
select cast('9.5' as decimal(10,3));
select cast('999.8788' as decimal(10,3));

-- 布尔型
select cast('y'::nchar as boolean);
select cast('1'::varchar as boolean);
select cast(1::int1 as boolean);
select cast('yes' as boolean);
select cast('n'::text as boolean);
select cast('0'::char as boolean);
select cast(0::tinyint as boolean);
select cast('false'::clob as boolean);
select cast(988::smallint as boolean);
select cast('000'::char as boolean);
select cast(-988::smallint as boolean);