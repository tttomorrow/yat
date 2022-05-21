-- @testpoint: alter system SET方法修改参数default_transaction_read_only为on，合理报错
--step1:查看默认值;expect:默认值是off
show default_transaction_read_only;
--step2:修改参数值为on;expect:报错
alter system SET default_transaction_read_only to on;