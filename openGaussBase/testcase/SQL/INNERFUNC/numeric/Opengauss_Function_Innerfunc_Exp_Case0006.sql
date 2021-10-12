-- @testpoint: exp函数入参范围校验，合理报错
select exp(709);
select exp(710);
select exp(-745);
select exp(-746);