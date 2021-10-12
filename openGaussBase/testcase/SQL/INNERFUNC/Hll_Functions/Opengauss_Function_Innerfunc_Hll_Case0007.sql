-- @testpoint: hll_hash_smallint(smallint, int32), 设置hash seed（即改变哈希策略）同时对smallint类型数据计算哈希值

select hll_hash_smallint(-32768, 10);
select hll_hash_smallint(32767, 0);