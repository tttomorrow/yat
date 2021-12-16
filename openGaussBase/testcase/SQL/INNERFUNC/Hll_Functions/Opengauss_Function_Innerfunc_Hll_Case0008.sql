-- @testpoint:  hll_hash_smallint(smallint, int32), 入参为其他类型时，合理报错

select hll_hash_smallint(-32769, 10);
select hll_hash_smallint(-32768, 2147483648);
select hll_hash_smallint('a', '214748364');
