-- @testpoint: opclass:操作符类:行存

--建表：行存
DROP TABLE if EXISTS tb1 CASCADE;
create table tb1(
c_int int,
c_float float4,
c_smalldatetime smalldatetime,
c_cidr cidr,
c_raw raw,
c_tsquery tsquery,
c_time time,
c_text text,
c_tsvector tsvector,
c_uuid uuid,
c_point point,
c_timestamp timestamp,
c_numeric numeric,
c_varchar varchar,
c_bytea bytea,
c_bool bool,
c_circle circle,
c_money money,
c_macaddr macaddr,
c_date date,
c_inet inet
);

--建索引指定操作符簇
create index idx_01 on tb1 using btree(c_int int4_ops) ;
create index idx_02 on tb1 using btree(c_float float4_ops) ;
create index idx_03 on tb1 using btree(c_smalldatetime smalldatetime_ops) ;
create index idx_04 on tb1 using btree(c_cidr cidr_ops) ;
create index idx_05 on tb1 using btree(c_raw raw_ops) ;
create index idx_06 on tb1 using btree(c_tsquery tsquery_ops) ;
create index idx_07 on tb1 using btree(c_time time_ops) ;
create index idx_08 on tb1 using btree(c_text text_ops) ;
create index idx_09 on tb1 using btree(c_tsvector tsvector_ops) ;
create index idx_10 on tb1 using btree(c_uuid uuid_ops) ;
create index idx_11 on tb1 using gist(c_point point_ops) ;
create index idx_12 on tb1 using btree(c_timestamp timestamp_ops) ;
create index idx_13 on tb1 using btree(c_numeric numeric_ops) ;
create index idx_14 on tb1 using btree(c_varchar varchar_ops) ;
create index idx_15 on tb1 using btree(c_bytea bytea_ops) ;
create index idx_16 on tb1 using btree(c_bool bool_ops) ;
create index idx_17 on tb1 using gist(c_circle circle_ops) ;
create index idx_18 on tb1 using btree(c_money money_ops) ;
create index idx_19 on tb1 using btree(c_macaddr macaddr_ops) ;
create index idx_21 on tb1 using btree(c_inet inet_ops) ;
select relname from pg_class where relname like 'idx_%' order by relname;


--行存临时表
DROP TABLE if EXISTS tb1 CASCADE;
create temporary table tb1(
c_int int,
c_float float4,
c_smalldatetime smalldatetime,
c_cidr cidr,
c_raw raw,
c_tsquery tsquery,
c_time time,
c_text text,
c_tsvector tsvector,
c_uuid uuid,
c_point point,
c_timestamp timestamp,
c_numeric numeric,
c_varchar varchar,
c_bytea bytea,
c_bool bool,
c_circle circle,
c_money money,
c_macaddr macaddr,
c_date date,
c_inet inet
);

--建索引指定操作符簇
create index idx_01 on tb1 using btree(c_int int4_ops) ;
create index idx_02 on tb1 using btree(c_float float4_ops) ;
create index idx_03 on tb1 using btree(c_smalldatetime smalldatetime_ops) ;
create index idx_04 on tb1 using btree(c_cidr cidr_ops) ;
create index idx_05 on tb1 using btree(c_raw raw_ops) ;
create index idx_06 on tb1 using btree(c_tsquery tsquery_ops) ;
create index idx_07 on tb1 using btree(c_time time_ops) ;
create index idx_08 on tb1 using btree(c_text text_ops) ;
create index idx_09 on tb1 using btree(c_tsvector tsvector_ops) ;
create index idx_10 on tb1 using btree(c_uuid uuid_ops) ;
create index idx_11 on tb1 using gist(c_point point_ops) ;
create index idx_12 on tb1 using btree(c_timestamp timestamp_ops) ;
create index idx_13 on tb1 using btree(c_numeric numeric_ops) ;
create index idx_14 on tb1 using btree(c_varchar varchar_ops) ;
create index idx_15 on tb1 using btree(c_bytea bytea_ops) ;
create index idx_16 on tb1 using btree(c_bool bool_ops) ;
create index idx_17 on tb1 using gist(c_circle circle_ops) ;
create index idx_18 on tb1 using btree(c_money money_ops) ;
create index idx_19 on tb1 using btree(c_macaddr macaddr_ops) ;
create index idx_21 on tb1 using btree(c_inet inet_ops) ;
select relname from pg_class where relname like 'idx_%' order by relname;


--行存分区表
DROP TABLE if EXISTS tb1 CASCADE;
create table tb1(
c_int int,
c_float float4,
c_smalldatetime smalldatetime,
c_cidr cidr,
c_raw raw,
c_tsquery tsquery,
c_time time,
c_text text,
c_tsvector tsvector,
c_uuid uuid,
c_point point,
c_timestamp timestamp,
c_numeric numeric,
c_varchar varchar,
c_bytea bytea,
c_bool bool,
c_circle circle,
c_money money,
c_macaddr macaddr,
c_date date,
c_inet inet
) WITH (ORIENTATION = row) partition by range(c_int)(
partition p1 values less than (100),
partition p2 values less than (1000),
partition p3 values less than (5000),
partition p4 values less than (10001)
);

--建索引指定操作符簇
create index idx_01 on tb1 using btree(c_int int4_ops) ;
create index idx_02 on tb1 using btree(c_float float4_ops) ;
create index idx_03 on tb1 using btree(c_smalldatetime smalldatetime_ops) ;
create index idx_04 on tb1 using btree(c_cidr cidr_ops) ;
create index idx_05 on tb1 using btree(c_raw raw_ops) ;
create index idx_06 on tb1 using btree(c_tsquery tsquery_ops) ;
create index idx_07 on tb1 using btree(c_time time_ops) ;
create index idx_08 on tb1 using btree(c_text text_ops) ;
create index idx_09 on tb1 using btree(c_tsvector tsvector_ops) ;
create index idx_10 on tb1 using btree(c_uuid uuid_ops) ;
create index idx_11 on tb1 using gist(c_point point_ops) local;
create index idx_12 on tb1 using btree(c_timestamp timestamp_ops) ;
create index idx_13 on tb1 using btree(c_numeric numeric_ops) ;
create index idx_14 on tb1 using btree(c_varchar varchar_ops) ;
create index idx_15 on tb1 using btree(c_bytea bytea_ops) ;
create index idx_16 on tb1 using btree(c_bool bool_ops) ;
create index idx_17 on tb1 using gist(c_circle circle_ops) local ;
create index idx_18 on tb1 using btree(c_money money_ops) ;
create index idx_19 on tb1 using btree(c_macaddr macaddr_ops) ;
create index idx_21 on tb1 using btree(c_inet inet_ops) ;
select relname from pg_class where relname like 'idx_%' order by relname;

--行存子自动拓展分区表
DROP TABLE if EXISTS tb1 CASCADE;
create table tb1(
c_int int,
c_float float4,
c_smalldatetime smalldatetime,
c_cidr cidr,
c_raw raw,
c_tsquery tsquery,
c_time time,
c_text text,
c_tsvector tsvector,
c_uuid uuid,
c_point point,
c_timestamp timestamp,
c_numeric numeric,
c_varchar varchar,
c_bytea bytea,
c_bool bool,
c_circle circle,
c_money money,
c_macaddr macaddr,
c_date date,
c_inet inet
) WITH (ORIENTATION = row) partition by range(c_timestamp) interval ('1 month') (
  partition part1 values less than ('1990-01-01 00:00:00')
);

--建索引指定操作符簇
create index idx_01 on tb1 using btree(c_int int4_ops) ;
create index idx_02 on tb1 using btree(c_float float4_ops) ;
create index idx_03 on tb1 using btree(c_smalldatetime smalldatetime_ops) ;
create index idx_04 on tb1 using btree(c_cidr cidr_ops) ;
create index idx_05 on tb1 using btree(c_raw raw_ops) ;
create index idx_06 on tb1 using btree(c_tsquery tsquery_ops) ;
create index idx_07 on tb1 using btree(c_time time_ops) ;
create index idx_08 on tb1 using btree(c_text text_ops) ;
create index idx_09 on tb1 using btree(c_tsvector tsvector_ops) ;
create index idx_10 on tb1 using btree(c_uuid uuid_ops) ;
create index idx_11 on tb1 using gist(c_point point_ops) local;
create index idx_12 on tb1 using btree(c_timestamp timestamp_ops) ;
create index idx_13 on tb1 using btree(c_numeric numeric_ops) ;
create index idx_14 on tb1 using btree(c_varchar varchar_ops) ;
create index idx_15 on tb1 using btree(c_bytea bytea_ops) ;
create index idx_16 on tb1 using btree(c_bool bool_ops) ;
create index idx_17 on tb1 using gist(c_circle circle_ops) local ;
create index idx_18 on tb1 using btree(c_money money_ops) ;
create index idx_19 on tb1 using btree(c_macaddr macaddr_ops) ;
create index idx_21 on tb1 using btree(c_inet inet_ops) ;
select relname from pg_class where relname like 'idx_%' order by relname;

--清理环境
DROP TABLE if EXISTS tb1 CASCADE;