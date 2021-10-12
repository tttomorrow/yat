-- @testpoint: set方法设置参数default_transaction_deferrable值为on
--查看默认
show default_transaction_deferrable;
--设置
set default_transaction_deferrable to on;
--查看
show default_transaction_deferrable;
--恢复默认
set default_transaction_deferrable to off;
show default_transaction_deferrable;