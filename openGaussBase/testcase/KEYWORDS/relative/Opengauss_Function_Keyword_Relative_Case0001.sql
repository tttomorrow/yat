--  @testpoint:openGauss鍏抽敭瀛梤elative(闈炰繚鐣?浣滀负鍒楀悕涓嶅甫鍙屽紩鍙凤紝relative澶у皬鍐欐贩鍚堬紝寤鸿〃鎴愬姛
drop table if exists relative_test;
create table relative_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	Relative text
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);
select * from relative_test;
drop table relative_test;

--openGauss鍏抽敭瀛梤elative(闈炰繚鐣?浣滀负鍒楀悕涓嶅甫鍙屽紩鍙凤紝relative澶у皬鍖归厤锛屽缓琛ㄦ垚鍔?
drop table if exists Collation_Catalog_test;
create table Collation_Catalog_test(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	relative text
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);
select * from Collation_Catalog_test;
drop table Collation_Catalog_test;