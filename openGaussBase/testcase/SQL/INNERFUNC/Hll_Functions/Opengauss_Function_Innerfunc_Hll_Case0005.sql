-- @testpoint: 函数hll_hash_smallint(smallint)，对smallint类型数据计算哈希值

select hll_hash_smallint(-32768);
select hll_hash_smallint(0);
select hll_hash_smallint(32767);
select hll_hash_smallint(true);
select hll_hash_smallint(false);