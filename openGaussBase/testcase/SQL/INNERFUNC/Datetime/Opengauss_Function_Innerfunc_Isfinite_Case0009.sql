--  @testpoint: isfinite timestamp类型只有年月日
drop table if exists test_date01;
create table test_date01 (clo1 timestamp without time zone );
insert into test_date01 values ('2001-02-16');
select isfinite(clo1) from test_date01;
SELECT isfinite(timestamp without time zone  '2001-02-16');
drop table if exists test_date01;