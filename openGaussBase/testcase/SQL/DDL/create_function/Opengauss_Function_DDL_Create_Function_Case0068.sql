-- @testpoint: 创建函数指定参数数据类型是日期时间型
create or replace function y_testfun8 (c_smalldatetime smalldatetime) returns date  as $$
        begin
                return (c_smalldatetime);
        end;
$$ language plpgsql;
/
--精确到分钟，秒位大于等于30秒进一位
call y_testfun8('2003-04-12 23:59:31');
--精确到分钟，秒位大于等于30秒进一位
call y_testfun8('2003-04-12 23:59:30');
--精确到分钟，秒位小于30秒，不进，秒数按0计算
call y_testfun8('2003-04-12 23:59:29');
--精确到分钟，秒位大于等于30秒进一位
call y_testfun8('2003-04-12 23:59:60');
drop function y_testfun8;
--创建函数指定参数数据类型是date
drop function if exists y_testfun9;
create function y_testfun9 (c_date date) returns date  as $$
        begin
                return (c_date);
        end;
$$ language plpgsql;
/
call y_testfun9('2020-8-10');
drop function  y_testfun9;