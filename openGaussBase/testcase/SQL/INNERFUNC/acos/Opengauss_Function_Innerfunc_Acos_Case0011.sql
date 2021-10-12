--  @testpoint:不同个数参数及类型测试(合理报错)


select acos() as result;
select acos(2  2) as result;
select acos(2,2) as result;
select acos(2)(2) as result;
select acos('abcd') as result;
select acos 1 as result;


