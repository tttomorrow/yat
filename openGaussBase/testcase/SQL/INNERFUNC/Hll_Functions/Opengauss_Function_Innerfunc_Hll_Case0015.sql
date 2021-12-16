-- @testpoint: hll_hash_bigint(bigint, int32),对bigint类型数据计算哈希值，并设置hashseed（即改变哈希策略）

select hll_hash_bigint(100::bigint, 2147483647);
select hll_hash_bigint(100::bigint, 0);
select hll_hash_bigint(-9223372036854775808, 10);
select hll_hash_bigint(9223372036854775807, 10);
select hll_hash_bigint(0, 0);