-- @testpoint: array_agg函数多参数少参数测试，合理报错
select array_agg(342321,5454) from sys_dummy;
select array_agg() from sys_dummy;
