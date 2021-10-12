-- @testpoint: covar_samp函数的参数类型测试，给定非double precision，合理报错
select covar_samp('1,343,565,78567,7865,45654','1,343,565,78567,7865,45654');
select covar_samp(3.4,'1,343,565,78567,7865,45654');
select covar_samp('1,343,565,78567,7865,45654',2.37);
select covar_samp('gtrgryttyuyifsdfa','gtrgryttyuyifsdfa');