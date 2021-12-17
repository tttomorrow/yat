-- @testpoint: hll_hash_bigint(bigint) 描述：对bigint类型数据计算哈希值

select hll_hash_bigint(-9223372036854775808);
select hll_hash_bigint(9223372036854775807);
select hll_hash_bigint(0);
select hll_hash_bigint(100::int::bigint);
