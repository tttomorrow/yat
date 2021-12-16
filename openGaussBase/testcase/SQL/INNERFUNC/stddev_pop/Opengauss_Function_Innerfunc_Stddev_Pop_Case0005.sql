-- @testpoint: 入参列只有一行数据时，返回0

drop table if exists stddec_tab_003;
create table stddec_tab_003(c1 smallint,c2 double precision,c3 real,c4 int,c5 binary_integer,c7 double precision,c8 bigint,c9 float, c10 numeric(12,6),c11 integer,c12 binary_double,c13 decimal(12,6),c14 number(12,6));

insert into stddec_tab_003 values(1,1.456789445455,3.1415926,1,'1',2.33,6.75844,-0.63,null,'',128.1452415,98*0.99,25563.1415);
insert into stddec_tab_003 values(3,1.45455,3.26,12,'1545',2.33,6.75844,-0.63,null,'',124.1452415,98*0.99,2563.1415);

select STDDEV_POP(c1),STDDEV_POP(c2),STDDEV_POP(c3),STDDEV_POP(c4),STDDEV_POP(c5),STDDEV_POP(c7),STDDEV_POP(c8),STDDEV_POP(c9),STDDEV_POP(c10),STDDEV_POP(c11),STDDEV_POP(c12),STDDEV_POP(c13),STDDEV_POP(c14) from stddec_tab_003;

drop table stddec_tab_003;