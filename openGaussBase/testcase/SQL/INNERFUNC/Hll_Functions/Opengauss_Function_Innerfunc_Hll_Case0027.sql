-- @testpoint:  hll_hash_any(anytype, int32) 对任意类型数据计算哈希值，并设置hashseed（即改变哈希策略）

select hll_hash_any ('clusterName'::text, 0);
SELECT hll_hash_any ('12.34'::float8::numeric::money,100);
select hll_hash_any ('clusterName'::char, 1);
select hll_hash_any ('[2010-01-01 14:30, 2010-01-01 15:30)'::tsrange, 10);
select hll_hash_any ('DEADBEEF'::raw, 15);
select hll_hash_any ('101'::bit, 0);
select hll_hash_any ('12-10-2010'::date, 60);
select hll_hash_any ('a fat cat sat on a mat and ate a fat rat'::tsvector, 30);
select hll_hash_any ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::uuid, 35);
select hll_hash_any (row_to_json(row(1,'foo')), 5);
select hll_hash_any (array_to_json('{{1,5},{99,100}}'::int[]), 16);