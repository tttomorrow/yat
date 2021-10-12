-- @testpoint: hll_hash_bytea(bytea),对bytea类型数据计算哈希值

select hll_hash_bytea('DEADBEEF');
select hll_hash_bytea('a');
select hll_hash_bytea('@##$');
select hll_hash_bytea('你好');