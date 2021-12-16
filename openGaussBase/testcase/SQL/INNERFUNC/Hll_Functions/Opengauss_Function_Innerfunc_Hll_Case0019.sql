-- @testpoint: hll_hash_bytea(bytea, int32),对bytea类型数据计算哈希值，并设置hashseed（即改变哈希策略）

select hll_hash_bytea(e'001001001', 12);
select hll_hash_bytea('DEADBEEF', 13);
select hll_hash_bytea('a', 16);
select hll_hash_bytea('@##$', 15);
select hll_hash_bytea('你好', 155);