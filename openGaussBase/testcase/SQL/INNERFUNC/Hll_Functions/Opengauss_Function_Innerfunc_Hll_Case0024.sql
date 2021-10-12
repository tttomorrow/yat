-- @testpoint: hll_hash_text(text, int32),入参为其他类型，合理报错

select hll_hash_text('ab', -1);
select hll_hash_text(天天开心, 10);
