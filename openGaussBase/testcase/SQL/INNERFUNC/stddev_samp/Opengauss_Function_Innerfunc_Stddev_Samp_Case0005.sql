-- @testpoint: 入参列只有一行数据时，返回空
drop table if exists stddec_tab_002;
create table stddec_tab_002
(
 c1  smallint,
 c2  double precision,
 c3  real, 
 c4  int,
 c5  binary_integer,
 c7  double precision,
 c8  bigint,
 c9  float,
 c10 numeric(12,6),
 c11 integer,
 c12 binary_double,
 c13 decimal(12,6),
 c14 number(12,6)
);
select STDDEV_SAMP(c1),STDDEV_SAMP(c2),STDDEV_SAMP(c3),STDDEV_SAMP(c4),STDDEV_SAMP(c5),STDDEV_SAMP(c7),STDDEV_SAMP(c8),STDDEV_SAMP(c9),STDDEV_SAMP(c10),STDDEV_SAMP(c11),STDDEV_SAMP(c12),STDDEV_SAMP(c13),STDDEV_SAMP(c14) from stddec_tab_002;
drop table if exists stddec_tab_002;
