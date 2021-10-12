-- @testpoint: set方法设置参数default_transaction_read_only为on，建表，合理报错
--查看默认
show default_transaction_read_only;
--set方法修改
set default_transaction_read_only to on;
--建表，报错
drop table if exists test_065;
create table test_065(id int);
--恢复参数默认值
set default_transaction_read_only to off;