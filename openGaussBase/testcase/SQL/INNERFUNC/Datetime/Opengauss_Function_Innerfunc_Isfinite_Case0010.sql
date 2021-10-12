--  @testpoint: isfinite timestamp类型的参数带时区
drop table if exists test_date01;
create table test_date01 (clo1 timestamp with time zone );
insert into test_date01 values ('2001-02-16 pst');
select isfinite(clo1) from test_date01;
SELECT isfinite(timestamp with time zone  '2001-02-16+08');
drop table if exists test_date01;