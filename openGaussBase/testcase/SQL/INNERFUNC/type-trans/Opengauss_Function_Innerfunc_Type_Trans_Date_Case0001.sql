-- @testpoint: 类型转换函数to_date(text)，将文本类型的值转换为指定格式的时间戳，入参为无效值时合理报错

select to_date('1999/1/8');
select to_date('19990108');
select to_date('1999-01-08');

select to_date('8-jan-99');
select to_date('1/8/1999');
select to_date('1/18/1999');
select to_date('1999-jan-08');
select to_date('jan-08-1999');
select to_date('8-jan-99');
select to_date('99-jan-08');
select to_date('8-jan-99');
select to_date('jan-08-99');
select to_date('990108');
select to_date('1999.008');
select to_date('j2451187');
select to_date('january 8, 99 bc');