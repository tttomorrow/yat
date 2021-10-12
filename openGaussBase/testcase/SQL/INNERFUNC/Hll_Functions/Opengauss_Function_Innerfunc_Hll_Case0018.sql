-- @testpoint: hll_hash_bytea(bytea),入参为其他类型时，合理报错

select hll_hash_bytea(@##$);
