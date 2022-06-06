-- @testpoint: 列存普通表，创建主键\唯一约束\唯一索引，验证超出支持字段数量，合理报错


--创建列存表，声明多字段(>32)，创建主键\唯一约束\唯一索引
--step1:创建普通列存表，声明多个字段，同时声明主键约束  expect:失败
drop table if exists t_columns_unique_index_0079_01;
create table t_columns_unique_index_0079_01(
id1 smallint, id2 integer, id3 decimal, id4 bigint, id5 tinyint,
id6 smallint, id7 integer, id8 decimal, id9 bigint, id10 tinyint,
id11 smallint, id12 integer, id13 decimal, id14 bigint, id15 tinyint,
id16 smallint, id17 integer, id18 decimal, id19 bigint, id20 tinyint,
id21 smallint, id22 integer, id23 decimal, id24 bigint, id25 tinyint,
id26 smallint, id27 integer, id28 decimal, id29 bigint, id30 tinyint,
id31 smallint, id32 integer, id33 decimal,
primary key(id1,id2,id3,id4,id5,id6,id7,id8,id9,id10,id11,id12,id13,id14,id15,id16,id17,id18,id19,id20,
id21,id22,id23,id24,id25,id26,id27,id28,id29,id30,id31,id32,id33)) with(orientation=column);

--step2:创建普通列存表，声明多个字段，同时声明唯一约束  expect:失败
drop table if exists t_columns_unique_index_0079_02;
create table t_columns_unique_index_0079_02(
id1 smallint, id2 integer, id3 decimal, id4 bigint, id5 tinyint,
id6 smallint, id7 integer, id8 decimal, id9 bigint, id10 tinyint,
id11 smallint, id12 integer, id13 decimal, id14 bigint, id15 tinyint,
id16 smallint, id17 integer, id18 decimal, id19 bigint, id20 tinyint,
id21 smallint, id22 integer, id23 decimal, id24 bigint, id25 tinyint,
id26 smallint, id27 integer, id28 decimal, id29 bigint, id30 tinyint,
id31 smallint, id32 integer, id33 decimal,
constraint const_79 unique(id1,id2,id3,id4,id5,id6,id7,id8,id9,id10,id11,id12,id13,id14,id15,id16,id17,id18,id19,id20,
id21,id22,id23,id24,id25,id26,id27,id28,id29,id30,id31,id32,id33)) with(orientation=column);

--step3:创建普通列存表，声明多个字段   expect:成功
drop table if exists t_columns_unique_index_0079_03;
create table t_columns_unique_index_0079_03(
id1 smallint, id2 integer, id3 decimal, id4 bigint, id5 tinyint,
id6 smallint, id7 integer, id8 decimal, id9 bigint, id10 tinyint,
id11 smallint, id12 integer, id13 decimal, id14 bigint, id15 tinyint,
id16 smallint, id17 integer, id18 decimal, id19 bigint, id20 tinyint,
id21 smallint, id22 integer, id23 decimal, id24 bigint, id25 tinyint,
id26 smallint, id27 integer, id28 decimal, id29 bigint, id30 tinyint,
id31 smallint, id32 integer, id33 decimal) with(orientation=column);

--step4:多字段创建唯一索引  expect:失败
create unique index i_columns_unique_index_0079 on t_columns_unique_index_0079_03 using btree(id1,id2,id3,id4,id5,id6,id7,id8,id9,id10,id11,id12,id13,id14,id15,id16,id17,id18,id19,id20,id21,id22,id23,id24,id25,id26,id27,id28,id29,id30,id31,id32,id33);

--step5:清理环境   expect:成功
drop table t_columns_unique_index_0079_03;

