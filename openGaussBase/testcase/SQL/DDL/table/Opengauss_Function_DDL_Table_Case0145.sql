-- @testpoint: 创建列类型是时间日期类型的表

SHOW datestyle;
SET datestyle='YMD';
DROP TABLE if exists date_type_tab;
CREATE TABLE date_type_tab (ab date,da time without time zone ,dai time with time zone,dfgh timestamp without time zone,dfga timestamp with time zone, vbg smalldatetime);
INSERT INTO date_type_tab VALUES ('2020-07-27','21:21:21','21:21:21 pst','2010-12-12','2013-12-11 pst','2003-04-12 04:05:06');
DROP TABLE if exists date_type_tab;
SHOW datestyle;
SET datestyle='MDY';
