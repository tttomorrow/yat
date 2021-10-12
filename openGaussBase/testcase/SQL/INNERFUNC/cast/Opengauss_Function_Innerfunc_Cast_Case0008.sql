-- @testpoint:验证cast函数是否支持distinct关键字 
select distinct cast(to_date('1989-06-16') as date);