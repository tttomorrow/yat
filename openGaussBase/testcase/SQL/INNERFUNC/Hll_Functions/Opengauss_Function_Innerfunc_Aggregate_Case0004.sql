-- @testpoint: hll_add_agg(hll_hashval, int32 log2m),入参为其他类型时，合理报错

select hll_add_agg(1215,10);
select hll_add_agg(hll_hash_boolean(true), 9);
select hll_add_agg(hll_hash_boolean(true), 'a');
select hll_add_agg (hll_hash_smallint(32767, 0), 17);