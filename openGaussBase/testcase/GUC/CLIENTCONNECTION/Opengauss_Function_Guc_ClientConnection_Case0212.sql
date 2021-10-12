-- @testpoint: set方法设置参数xloginsert_locks，合理报错
--查看默认
show xloginsert_locks;
--设置，报错
set xloginsert_locks to 7;
--no need to clean