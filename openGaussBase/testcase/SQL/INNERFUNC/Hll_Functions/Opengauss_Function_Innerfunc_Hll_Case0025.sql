-- @testpoint: hll_hash_any(anytype), 对任意类型数据计算哈希值

select hll_hash_any(1223265);
select hll_hash_any('08:00:2b:01:02:03'::macaddr);
select hll_hash_any ('clusterName'::text);
SELECT hll_hash_any ('12.34'::float8::numeric::money);
select hll_hash_any ('clusterName'::char);
select hll_hash_any ('[2010-01-01 14:30, 2010-01-01 15:30)'::tsrange);
select hll_hash_any ('DEADBEEF'::raw);
select hll_hash_any ('101'::bit);
select hll_hash_any ('12-10-2010'::date);
select hll_hash_any ('a fat cat sat on a mat and ate a fat rat'::tsvector);
select hll_hash_any ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::uuid);
select hll_hash_any (row_to_json(row(1,'foo')));
select hll_hash_any (array_to_json('{{1,5},{99,100}}'::int[]));