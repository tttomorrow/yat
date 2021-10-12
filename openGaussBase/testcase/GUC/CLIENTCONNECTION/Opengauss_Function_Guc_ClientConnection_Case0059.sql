-- @testpoint: set方法设置参数值为有效值
--查看默认
show default_transaction_isolation;
--设置
set default_transaction_isolation to 'repeatable read';
show default_transaction_isolation;
set default_transaction_isolation to 'serializable';
show default_transaction_isolation;
--恢复默认
set default_transaction_isolation to 'read committed';
show default_transaction_isolation;