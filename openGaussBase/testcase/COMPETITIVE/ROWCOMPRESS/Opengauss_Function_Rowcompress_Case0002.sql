-- @testpoint: 行存压缩表:指定压缩类型参数为zstd，验证创建表时参数组合，部分step合理报错

--test1: 创建行存压缩表：使用参数compresstype=2，其他压缩参数正常
--step1: 创建行存压缩表，parameter compresstype=2; expect:成功
drop table if exists t_rowcompress_0002 cascade;
create table t_rowcompress_0002(cid int, name varchar2) with (compresstype=2);
--step2: 创建行存压缩表，parameter compress_level=1; expect:成功
drop table if exists t_rowcompress_0002 cascade;
create table t_rowcompress_0002(cid int, name varchar2) with (compresstype=2, compress_level=1);
--step3: 创建行存压缩表，parameter compress_chunk_size=1/4BLCKSZ; expect:成功
drop table if exists t_rowcompress_0002 cascade;
create table t_rowcompress_0002(cid int, name varchar2) with (compresstype=2, compress_chunk_size=2048);
--step4: 创建行存压缩表，parameter compress_prealloc_chunks=1; expect:成功
drop table if exists t_rowcompress_0002 cascade;
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_prealloc_chunks=1);
--step5: 创建行存压缩表，parameter compress_byte_convert=true; expect:成功
drop table if exists t_rowcompress_0002 cascade;
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_byte_convert=true);
--step6: 创建行存压缩表，parameter compress_byte_convert=true, compress_diff_convert=true; expect:成功
drop table if exists t_rowcompress_0002 cascade;
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_diff_convert=true, compress_byte_convert=true);
--step7: 创建行存压缩表，parameter compress_level=1, compress_chunk_size=1/16BLCKSZ, compress_prealloc_chunks=7, compress_byte_convert=true, compress_diff_convert=true; expect:成功
drop table if exists t_rowcompress_0002 cascade;
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_level=1, compress_chunk_size=512, compress_prealloc_chunks=7, compress_diff_convert=true, compress_byte_convert=true);

--test2: 创建行存压缩表：使用参数compresstype=2，其他压缩参数异常
--step8: 创建行存压缩表，parameter compress_chunk_size=1/3BLCKSZ; expect:合理报错
drop table if exists t_rowcompress_0002 cascade;
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_chunk_size=1000);
--step9: 创建行存压缩表，parameter compress_chunk_size=abc; expect:合理报错
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_chunk_size=abc);
--step10: 创建行存压缩表，parameter compress_level=32; expect:合理报错
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_level=32);
--step11: 创建行存压缩表，parameter compress_level==abc; expect:合理报错
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_level=abc);
--step12: 创建行存压缩表，parameter compress_prealloc_chunks=2; expect:合理报错
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_prealloc_chunks=2);
--step13: 创建行存压缩表，parameter compress_chunk_size=1/8BLCKSZ, compress_prealloc_chunks=8; expect:合理报错
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_chunk_size=1024, compress_prealloc_chunks=8);
--step14: 创建行存压缩表，parameter compress_prealloc_chunks=abc; expect:合理报错
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_prealloc_chunks=abc);
--step15: 创建行存压缩表，parameter compress_diff_convert=true; expect:合理报错
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_diff_convert=true);
--step16: 创建行存压缩表，parameter compress_byte_convert=100; expect:合理报错
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_byte_convert=100);
--step17: 创建行存压缩表，parameter compress_byte_convert=abc; expect:合理报错
create table t_rowcompress_0002(cid int, name varchar2) with(compresstype=2, compress_byte_convert=abc);

--step18: 删除行存压缩表
drop table if exists t_rowcompress_0002 cascade;