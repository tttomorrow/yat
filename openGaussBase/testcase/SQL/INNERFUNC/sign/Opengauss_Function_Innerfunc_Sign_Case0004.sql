-- @testpoint: sign函数多参少参校验，合理报错
select sign(9,6);
select sign('9','6');
select sign();