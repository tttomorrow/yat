--  @testpoint:创建函数，指定函数的语言的名称是SQL,函数体内使用select语句
drop FUNCTION if EXISTS add_em(integer, integer);
--声明基本类型作为函数的参数
CREATE FUNCTION add_em(integer, integer) RETURNS integer AS $$
        SELECT $1 + $2;
    $$ LANGUAGE SQL;
 /
  SELECT add_em(1,2) AS answer;
  drop FUNCTION add_em;