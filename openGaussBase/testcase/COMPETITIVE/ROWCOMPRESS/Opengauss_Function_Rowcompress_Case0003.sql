-- @testpoint: 行存压缩表:验证非法参数组合，合理报错

--step1: 创建表时指定参数 orientation=COLUMN，compresstype=1(pglz);
drop table if exists t_rowcompress_0003 cascade;
create table t_rowcompress_0003(cid int, name varchar2) with(orientation=COLUMN, compresstype=1);
--step2: 创建表时指定参数 orientation=COLUMN，compresstype=2(zstd);
create table t_rowcompress_0003(cid int, name varchar2) with(orientation=COLUMN, compresstype=2);
--step3: 创建表时指定参数 orientation=COLUMN，compress_chunk_size=1/4BLCKSZ;
create table t_rowcompress_0003(cid int, name varchar2) with(orientation=COLUMN, compress_chunk_size=2048);
--step4: 创建表时指定参数 orientation=COLUMN，compress_byte_convert=true;
create table t_rowcompress_0003(cid int, name varchar2) with(orientation=COLUMN, compress_byte_convert=true);
--step5: 创建表时不指定压缩类型，parameter compress_level=1;
create table t_rowcompress_0003(cid int, name varchar2) with(compress_level=1);
--step6: 创建表时不指定压缩类型，parameter compress_chunk_size=1/4BLCKSZ;
create table t_rowcompress_0003(cid int, name varchar2) with(compress_chunk_size=2048);
--step7: 创建表时不指定压缩类型，parameter compress_prealloc_chunks=1;
create table t_rowcompress_0003(cid int, name varchar2) with(compress_prealloc_chunks=1);
--step8: 创建表时不指定压缩类型，parameter compress_byte_convert=true;
create table t_rowcompress_0003(cid int, name varchar2) with(compress_byte_convert=true);
--step9: 创建行存压缩表，parameter compress_diff_convert=true;
create table t_rowcompress_0003(cid int, name varchar2) with(compress_diff_convert=true);
--step10：删除行存压缩表
drop table if exists t_rowcompress_0003 cascade;