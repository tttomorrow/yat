-- @testpoint: 创建表时使用compress关键字,合理报错
drop table if exists t_warehouse_t1;
create table t_warehouse_t1( w_warehouse_sk int not null,w_warehouse_id char(16) ,
w_warehouse_name  varchar(20)) compress;
