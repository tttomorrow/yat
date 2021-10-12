-- @testpoint: 创建函数指定模式名（模式名已存在）

drop schema if exists self cascade;
CREATE schema self;
drop FUNCTION if exists self.sum_two(integer, integer);
CREATE FUNCTION self.sum_two(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/

select proname from pg_proc where proname='sum_two';
drop FUNCTION self.sum_two(integer, integer);
drop schema self cascade;