-- @testpoint: 获取约束的定义
DROP table IF EXISTS warehouse_t2;
CREATE TABLE warehouse_t2(W_WAREHOUSE_SK  INTEGER    UNIQUE DEFERRABLE);
select pg_get_constraintdef(oid) from PG_CONSTRAINT where  conname = 'warehouse_t2_w_warehouse_sk_key' ;
DROP table IF EXISTS warehouse_t2;