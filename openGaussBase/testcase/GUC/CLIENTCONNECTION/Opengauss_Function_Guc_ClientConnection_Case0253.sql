-- @testpoint: ALTER SYSTEM SET方法设置max_locks_per_transaction参数为无效值，合理报错
--查看默认
show max_locks_per_transaction;
--设置，报错
ALTER SYSTEM SET max_locks_per_transaction to 9;
ALTER SYSTEM SET max_locks_per_transaction to 'test';
ALTER SYSTEM SET max_locks_per_transaction to 182.589;
ALTER SYSTEM SET max_locks_per_transaction to '10&%$#';
ALTER SYSTEM SET max_locks_per_transaction to '';
--no need to clean