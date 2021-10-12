-- @testpoint: replace函数异常校验，合理报错
select replace('woand') as result from sys_dummy;
select replace('woand','wo','you',null) as result from sys_dummy;
select replace() as result from sys_dummy;
