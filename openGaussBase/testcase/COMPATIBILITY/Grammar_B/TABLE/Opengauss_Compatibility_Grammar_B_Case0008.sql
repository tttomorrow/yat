-- @testpoint: 删除分区表索引添加on table
--step1:建表;expect:成功
drop table if exists tb_plugin0008 cascade;
drop index if exists id_plugin0008_01,id_plugin0008_02;
drop tablespace if exists tsp_idx0008;
create tablespace tsp_idx0008 relative location 'tablespace/tsp_idx0008';
create table tb_plugin0008
(
c_integer integer,
c_smallint smallint,
c_bigint bigint,
c_decimal decimal,
c_numeric numeric,
c_real real,
c_double  double precision,
c_character_1 character varying(100),
c_varchar varchar(100),
c_character_2 character(100),
c_char_1 char(100),
c_character_3 character,
c_char_2 char,
c_text text,
c_nvarchar2 nvarchar2,
c_name text,
c_timestamp_1 timestamp without time zone ,
c_timestamp_2 timestamp with time zone,
c_date date,
c_tsvector text,
c_tsquery text
) with (storage_type=ustore)
partition by range(c_integer)
(
partition p1 values less than (50000),
partition p2 values less than (100000),
partition p3 values less than (150000)
);

--step2:分区表创建local 索引;expect:成功
insert into tb_plugin0008 values(generate_series(1,140000),10,100,100.3,10,10.2,1000.25,'abcd','ABCD','ABC','DEF','A','A','HK','OLUMNAR_STORAGE','b','1954-2-6 00:00:30+8','1954-2-6 23:12:12.2356','1954-2-6 13:12:12.2356','abc db','ege');
create index id_plugin0008_01 on tb_plugin0008(c_integer desc) local with (indexsplit=insertpt) tablespace tsp_idx0008;
create index id_plugin0008_02 on tb_plugin0008 using ubtree(c_bigint DESC) local;

--step3:删除索引;expect:成功
drop index id_plugin0008_01 on tb_plugin0008;
drop index id_plugin0008_02 on id_plugin0008;

--step4:创建global索引;expect:成功
drop index if exists id_plugin0008_03;
CREATE INDEX id_plugin0008_03 ON tb_plugin0008(c_character_2) GLOBAL;
--step5:删除索引;expect:成功
drop index id_plugin0008_03 on tb_plugin0008;

--step6:清理环境;expect:成功
drop table if exists tb_plugin0008 cascade;
drop tablespace if exists tsp_idx0008;
