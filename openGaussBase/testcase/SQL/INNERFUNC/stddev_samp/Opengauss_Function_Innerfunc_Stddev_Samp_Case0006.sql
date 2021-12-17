-- @testpoint: 结合聚集函数，入参为表达式

drop table if exists stddec_tab_006;
create table stddec_tab_006(c1 smallint,c2 double precision,c3 real,c4 int,c5 binary_integer);
insert into stddec_tab_006 values(1,1.456789445455,3.1415926,1,2.33);
insert into stddec_tab_006 values(2,2.33355,3.1415926,1,2.33);
insert into stddec_tab_006 values(3,3.456789,3.1415926,1,2.33);
insert into stddec_tab_006 values(4,0.456789445455,3.1415926,1,2.33);
insert into stddec_tab_006 values(5,2.456789445455,3.1415926,1,2.33);
select STDDEV_SAMP(abs(c1)),STDDEV_SAMP(sin(c2)),STDDEV_SAMP(cos(c3)),STDDEV_SAMP(sqrt(c4)),STDDEV_SAMP(c5) from stddec_tab_006;
drop table stddec_tab_006;
