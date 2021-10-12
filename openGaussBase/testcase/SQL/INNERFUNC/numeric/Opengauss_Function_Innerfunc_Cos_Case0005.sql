-- @testpoint: cos函数与参数个数及类型校验，合理报错
select cos(2*pi(),2*pi()));
select cos();
select cos('yeah');