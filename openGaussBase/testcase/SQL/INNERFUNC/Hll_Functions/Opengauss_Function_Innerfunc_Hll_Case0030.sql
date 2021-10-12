-- @testpoint: hll_hashval_eq(hll_hashval, hll_hashval), 当入参为非hll_hashval类型时，合理报错

select hll_hashval_eq(hll_hash_integer(1),basicemailmasking('abcd@gmail.com'));
