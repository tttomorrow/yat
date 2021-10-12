-- @testpoint: covar_samp函数入参是空值的验证
select covar_samp('','');
select covar_samp(null,null);
select covar_samp(''+null,''+null);
select covar_samp(''*null/null,''*null/null);