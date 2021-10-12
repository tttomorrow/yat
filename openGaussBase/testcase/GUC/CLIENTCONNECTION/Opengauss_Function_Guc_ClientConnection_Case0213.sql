-- @testpoint: alter system set方法设置参数xloginsert_locks为无效值，合理报错
--查看默认
show xloginsert_locks;
--设置为超临界值，报错
alter system set xloginsert_locks to 0;
alter system set xloginsert_locks to 1001;
--设置浮点型，报错
ALTER SYSTEM SET xloginsert_locks to 1582.256;
--设置字符型，报错
ALTER SYSTEM SET xloginsert_locks to 'test';
ALTER SYSTEM SET xloginsert_locks to '20%$#';
--设置空串，报错
ALTER SYSTEM SET xloginsert_locks to '';
ALTER SYSTEM SET xloginsert_locks to 'null';
--no need to clean