--  @testpoint:不同参数个数及类型测试（合理报错）

select asin() as result;
select asin(2  2) as result;
select asin(2,2) as result;
select asin(2)(2) as result;
select asin('abcd') as result;
select asin 1 as result;



