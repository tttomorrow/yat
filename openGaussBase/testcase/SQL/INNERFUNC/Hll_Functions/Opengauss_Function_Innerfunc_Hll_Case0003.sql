-- @testpoint: 函数hll_hash_boolean(bool, int32) 设置hash seed（即改变哈希策略）并对bool类型数据计算哈希值

select hll_hash_boolean(true, 0);
select hll_hash_boolean('t', 0);
select hll_hash_boolean(1, 8);
select hll_hash_boolean('1', 8);
select hll_hash_boolean('y', 7);
select hll_hash_boolean('yes', 7);

select hll_hash_boolean(false, 0);
select hll_hash_boolean('f', 0);
select hll_hash_boolean(0, 5);
select hll_hash_boolean('0', 5);
select hll_hash_boolean('n', 4);
select hll_hash_boolean('no', 4);
select hll_hash_boolean(true, true);
select hll_hash_boolean(false, false);
