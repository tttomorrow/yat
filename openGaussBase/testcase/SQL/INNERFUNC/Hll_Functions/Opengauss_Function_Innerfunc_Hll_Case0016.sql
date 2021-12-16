-- @testpoint: hll_hash_bigint(bigint, int32),当入参为其他类型时,合理报错

select hll_hash_bigint(100::bigint, -2147483648);
select hll_hash_bigint(100::bigint, 2147483648);
select hll_hash_bigint(-2147483649, 2147483648);
select hll_hash_bigint(0, -2147483649);