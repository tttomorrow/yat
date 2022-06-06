-- @testpoint: set方法设置参数max_pred_locks_per_transaction,合理报错
--查看默认
show max_pred_locks_per_transaction;
--设置，报错
set max_pred_locks_per_transaction to 2147483647;
set max_pred_locks_per_transaction to 10;
--no need to clean