-- @testpoint: ALTER SYSTEM SET方法设置参数值default_transaction_deferrable为on，合理报错
--查看默认
show default_transaction_deferrable;
--修改，报错
ALTER SYSTEM SET default_transaction_deferrable to on;
--no need to clean