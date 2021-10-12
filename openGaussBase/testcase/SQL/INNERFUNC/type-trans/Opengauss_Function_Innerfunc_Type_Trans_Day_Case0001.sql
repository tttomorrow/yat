-- @testpoint: 类型转换函数numtoday(numeric)，数字类型的值转换为指定格式的时间戳。

select numtoday(20);
select numtoday('98');
select numtoday(2020);
select numtoday('2020'::nchar);
select numtoday('2020'::varchar);
select numtoday('123456.12354');
select numtoday('20.2'::numeric(9,3));