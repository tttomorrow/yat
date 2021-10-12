-- @testpoint: hll_hash_integer(integer),入参为非integer类型时,合理报错

select hll_hash_integer('yes');