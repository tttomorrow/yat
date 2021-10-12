-- @testpoint:验证cast函数是否能够将日期类型转为字符型
select cast(to_date('2020-02-01') as char);