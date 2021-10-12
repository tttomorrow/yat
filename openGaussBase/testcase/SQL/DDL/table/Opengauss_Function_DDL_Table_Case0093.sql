-- @testpoint: 列存表的表级外键约束，不支持合理报错
DROP TABLE IF EXISTS example;
DROP TABLE IF EXISTS t1 ;
--ERROR:  column/timeseries store unsupport constraint "PRIMARY KEY"
CREATE TABLE example (
        a integer,
        b integer,
        c integer,
        PRIMARY KEY (b, c)
    )with(ORIENTATION=COLUMN);


--ERROR:  FOREIGN KEY ... REFERENCES constraint is not yet supported.
CREATE TABLE t1 (
        a integer PRIMARY KEY,
        b integer,
        c integer,
        FOREIGN KEY (b, c) REFERENCES example (b, c)
    )with(ORIENTATION=COLUMN);
DROP TABLE IF EXISTS example;