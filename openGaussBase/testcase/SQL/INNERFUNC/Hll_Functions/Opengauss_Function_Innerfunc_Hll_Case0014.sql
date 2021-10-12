-- @testpoint: hll_hash_bigint(bigint),当入参为其他类型时，合理报错

select hll_hash_bigint('aaa');
select hll_hash_bigint('@');