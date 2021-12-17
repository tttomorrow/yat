-- @testpoint: hll_hash_integer(integer, int32),当入参类型为其他类型时，合理报错

select hll_hash_integer(-2147483649, 10);
select hll_hash_integer(2147483648, 2147483647);
select hll_hash_integer('a', 2147483647);
select hll_hash_integer(111, 2147483648);
select hll_hash_integer(111, 'a');