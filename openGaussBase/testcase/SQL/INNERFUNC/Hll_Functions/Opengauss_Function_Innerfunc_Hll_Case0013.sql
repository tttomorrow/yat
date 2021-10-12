-- @testpoint: hll_hash_bigint(bigint) 描述：对bigint类型数据计算哈希值

select hll_hash_bigint(0);
select hll_hash_bigint(100::int::bigint);
