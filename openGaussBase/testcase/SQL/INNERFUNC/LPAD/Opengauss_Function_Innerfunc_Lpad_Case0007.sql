-- @testpoint: lpad函数参数异常校验，合理报错
select lpad();
select lpad(null);
select lpad(0);
select lpad(' ');