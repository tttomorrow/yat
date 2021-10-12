-- @testpoint: hll_hash_integer(integer, int32) 对integer类型数据计算哈希值，并设置hashseed（即改变哈希策略）

select hll_hash_integer(0, 0);