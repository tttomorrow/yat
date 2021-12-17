-- @testpoint: 类型转换函数numtoday(numeric)，数字类型的值转换为指定格式的时间戳，入参为无效值时合理报错

select numtoday(' ');

select numtoday(12345678987654321);

select numtoday(2f);

select numtoday(@#$);

select numtoday('二');

select numtoday('20.2'::numeric(1,3));

select numtoday('200.2'::numeric(2,1));