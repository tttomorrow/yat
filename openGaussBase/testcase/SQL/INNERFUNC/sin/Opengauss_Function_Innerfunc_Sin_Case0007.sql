-- @testpoint: 输入参数为多个,合理报错

select sin(2  2) as result;
select sin(2,2) as result;
select sin(2)(2) as result;