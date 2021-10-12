-- @testpoint: covar_samp函数参数个数的校验，多参少参合理报错
select covar_samp(1,343,565,78567,7865,45654);
select covar_samp();
select covar_samp('',null,null);