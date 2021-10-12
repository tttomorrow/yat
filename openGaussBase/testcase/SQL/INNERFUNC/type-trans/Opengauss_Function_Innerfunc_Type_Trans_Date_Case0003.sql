-- @testpoint: 类型转换函数to_date(text, text)，字符串类型的值转换为指定格式的日期，入参为有效值

select to_date('05 Dec 2000', 'DD Mon YYYY');
select to_date('05 Dec 2000', 'DD-Mon-YYYY');
select to_date('05 Dec 2000', 'DD/Mon/YYYY');
select to_date('05 Dec 2000', 'DD/Mon/YYYY');
select to_date('05 December 2000', 'DD/MONTH/YYYY');
select to_date('1999/1/8','YYYY/MM/DD');
select to_date('1999/1/8','YYYY-MM-DD');
select to_date('19990108','YYYYMMDD');
select to_date('1999-01-08','YYYY/MM/DD');
select to_date('1/8/1999', 'DD MM YYYY');
select to_date('1/08/1999', 'MM DD YYYY');
select to_date('1999-Jan-08', 'YYYY-Mon-DD');
select to_date('Jan-08-1999', 'Mon DD YYYY');
select to_date('8-Jan-99', 'DD Mon YY');
select to_date('99-Jan-08', 'YY Mon DD');
select to_date('8-Jan-99', 'DD Mon YY');
select to_date('Jan-08-99', 'Mon DD YY');
select to_date('1999.008', 'YYYY DDD');
select to_date('January 8, 99 BC', 'MONTH DD, YY BC');
select to_date('990108', 'YY MM DD');
select to_date('8-Jan-99', 'DD Mon YY');
select to_date('1999 2 28','YYYY-MM-DD');


