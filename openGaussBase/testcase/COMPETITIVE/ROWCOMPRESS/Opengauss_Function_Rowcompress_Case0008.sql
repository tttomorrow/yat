-- @testpoint: 修改行存压缩索引参数，部分step合理报错

--step1: 创建行存压缩索引：使用参数compresstype=1
drop table if exists t_rowcompress_0008 cascade;
create table t_rowcompress_0008(cid int, name varchar2) with (compresstype=1);
create index i_rowcompress_0008 on t_rowcompress_0008(name) with (compresstype=1);
--step2: 修改行存压缩参数，parameter compresstype=2;
alter index i_rowcompress_0008 set (compresstype=2);
--step3: 修改行存压缩参数，parameter compress_level=7;
alter index i_rowcompress_0008 set (compress_level=7);
--step4: 修改行存压缩参数，parameter compress_chunk_size=1/4BLCKSZ;
alter index i_rowcompress_0008 set (compress_chunk_size=2048);
--step5: 修改行存压缩参数，parameter compress_prealloc_chunks=1;
alter index i_rowcompress_0008 set (compress_prealloc_chunks=1);
--step6: 修改行存压缩参数，parameter compress_prealloc_chunks=5;
alter index i_rowcompress_0008 set (compress_prealloc_chunks=5);
--step7: 修改行存压缩参数，parameter compress_diff_convert=true;
alter index i_rowcompress_0008 set (compress_diff_convert=true);
--step8: 修改行存压缩参数，parameter compress_byte_convert=true;
alter index i_rowcompress_0008 set (compress_byte_convert=true);
--step9: 修改行存压缩参数，parameter compress_diff_convert=true;
alter index i_rowcompress_0008 set (compress_diff_convert=true);

--step10: 删除行存压缩索引
drop index if exists i_rowcompress_0008 cascade;
--step11: 创建行存压缩索引：使用参数compresstype=2, compress_chunk_size=1/4BLCKSZ);
create index i_rowcompress_0008 on t_rowcompress_0008(name) with (compresstype=2, compress_chunk_size=2048);
--step12: 修改行存压缩参数，parameter compresstype=1;
alter index i_rowcompress_0008 set (compresstype=1);
--step13: 修改行存压缩参数，parameter compress_level=3;
alter index i_rowcompress_0008 set (compress_level=3);
--step14: 修改行存压缩参数，parameter compress_chunk_size=1/2BLCKSZ;
alter index i_rowcompress_0008 set (compress_chunk_size=4096);
--step15: 修改行存压缩参数，parameter compress_prealloc_chunks=3;
alter index i_rowcompress_0008 set (compress_prealloc_chunks=3);
--step16: 修改行存压缩参数，parameter compress_diff_convert=true;
alter index i_rowcompress_0008 set (compress_diff_convert=true);
--step17: 修改行存压缩参数，parameter compress_byte_convert=true;
alter index i_rowcompress_0008 set (compress_byte_convert=true);
--step18: 修改行存压缩参数，parameter compress_diff_convert=true;
alter index i_rowcompress_0008 set (compress_diff_convert=true);

--step19: 删除行存压缩表
drop table if exists t_rowcompress_0008 cascade;