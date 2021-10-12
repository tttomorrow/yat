-- @testpoint: 匿名块中for loop 语句插入大量数据

declare
  v_lang clob := 'charuhailiangzifu';
begin
	raise notice '%',length(v_lang);
  for i in 1 .. 1928 loop
    v_lang := v_lang || 'charuhailiangzifu';
  end loop;
	raise notice '%',v_lang;
	raise notice '%',length(v_lang);
end;
/



