-- @testpoint: hll_add_agg(hll_hashval),把哈希后的数据按照分组放到hll中,当入参为其他类型时,合理报错

select hll_add_agg(1215);

