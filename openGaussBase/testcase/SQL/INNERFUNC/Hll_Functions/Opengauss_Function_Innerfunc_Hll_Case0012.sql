-- @testpoint: hll_hash_integer(integer, int32),当入参类型为其他类型时，合理报错

select hll_hash_integer(111, 'a');