-- @testpoint: DQL语法，结合操作符

drop table if exists t_long_or_t12;
drop table if exists t_long_or_t32;
create table t_long_or_t12(F_INT1 int , F_INT2 varchar(100));
create table t_long_or_t32(F_INT1 int , F_INT2 varchar(100));

INSERT INTO t_long_or_t12(F_INT1, F_INT2) VALUES(200,'a');
INSERT INTO t_long_or_t12(F_INT1, F_INT2) VALUES(250,'b');
INSERT INTO t_long_or_t12(F_INT1, F_INT2) VALUES(360,'c');
INSERT INTO t_long_or_t12(F_INT1, F_INT2) VALUES(700,'d');
INSERT INTO t_long_or_t12(F_INT1, F_INT2) VALUES(1000,'e');
INSERT INTO t_long_or_t12(F_INT1, F_INT2) VALUES(2000,'f');
INSERT INTO t_long_or_t32(F_INT1, F_INT2) VALUES(100,'r');
INSERT INTO t_long_or_t32(F_INT1, F_INT2) VALUES(198,'d');
INSERT INTO t_long_or_t32(F_INT1, F_INT2) VALUES(600,'ed');
INSERT INTO t_long_or_t32(F_INT1, F_INT2) VALUES(800,'red');
INSERT INTO t_long_or_t32(F_INT1, F_INT2) VALUES(1999,'rll');
INSERT INTO t_long_or_t32(F_INT1, F_INT2) VALUES(2399,'lo');


select F_INT2 from t_long_or_t12 where F_INT1>1000 or (F_INT1<500 and F_INT1>275);
select F_INT2 from t_long_or_t32 where F_INT1 > 1000 or (275 < F_INT1 and F_INT1 < 500);
select F_INT2 from t_long_or_t32 where F_INT1 != 1000 and F_INT1 >= 500;

drop table t_long_or_t12;
drop table t_long_or_t32;