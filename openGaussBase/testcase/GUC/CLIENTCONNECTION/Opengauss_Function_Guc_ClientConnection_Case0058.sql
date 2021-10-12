-- @testpoint: alter system set方法设置参数default_transaction_isolation值，合理报错
--查看默认
show default_transaction_isolation;
--修改，报错
alter system set default_transaction_isolation to 'repeatable read';
alter system set default_transaction_isolation to 'serializable';