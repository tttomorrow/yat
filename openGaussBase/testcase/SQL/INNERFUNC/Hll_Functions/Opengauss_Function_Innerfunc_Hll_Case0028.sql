-- @testpoint: hll_hash_any(anytype, int32),当入参2为其他类型时,合理报错

select hll_hash_any ('101'::bit, -1);