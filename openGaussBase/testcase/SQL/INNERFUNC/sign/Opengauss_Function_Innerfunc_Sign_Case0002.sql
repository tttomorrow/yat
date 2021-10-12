-- @testpoint: sign函数非法值校验，合理报错
select sign(r);
select sign(~);
select sign('a');
