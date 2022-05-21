-- @testpoint: 行存压缩索引:验证非法参数组合，合理报错

drop table if exists t_rowcompress_0006 cascade;
create table t_rowcompress_0006(cid int, name varchar2) with(compresstype=2);
--step1: 创建索引时不指定压缩类型，parameter compress_level=1;
create index i_rowcompress_0006 on t_rowcompress_0006(name) with(compress_level=1);
--step2: 创建索引时不指定压缩类型，parameter compress_chunk_size=1/4BLCKSZ;
create index i_rowcompress_0006 on t_rowcompress_0006(name) with(compress_chunk_size=2048);
--step3: 创建索引时不指定压缩类型，parameter compress_prealloc_chunks=1;
create index i_rowcompress_0006 on t_rowcompress_0006(name) with(compress_prealloc_chunks=1);
--step4: 创建索引时不指定压缩类型，parameter compress_byte_convert=true;
create index i_rowcompress_0006 on t_rowcompress_0006(name) with(compress_byte_convert=true);
--step5: 创建行存压缩索引，parameter compress_diff_convert=true;
create index i_rowcompress_0006 on t_rowcompress_0006(name) with(compress_diff_convert=true);
--step6: 创建行存压缩索引，索引类型为gin
create index i_rowcompress_0006 on t_rowcompress_0006 using gin(name) with (compresstype=1);
--step7: 创建行存压缩索引，索引类型为gist
create index i_rowcompress_0006 on t_rowcompress_0006 using gist(name) with (compresstype=1);
--step8: 创建行存压缩索引，索引类型为psort
create index i_rowcompress_0006 on t_rowcompress_0006 using psort(name) with (compresstype=1);
--step9：删除行存压缩表
drop table if exists t_rowcompress_0006 cascade;