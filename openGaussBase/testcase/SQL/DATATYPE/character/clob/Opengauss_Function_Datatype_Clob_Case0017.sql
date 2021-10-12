--  @testpoint:clob：to_char (string)：clob值的其他场景：success
select to_char(to_clob(''));
select to_char(to_clob(' '));
select to_char(to_clob(null));